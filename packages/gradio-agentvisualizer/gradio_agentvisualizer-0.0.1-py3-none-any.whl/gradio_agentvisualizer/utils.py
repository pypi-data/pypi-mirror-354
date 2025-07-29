import gradio as gr
import json
import time

def agent_to_dict(agent, name=None):
    return {
        "name": f"{name} | {agent.__class__.__name__} | {agent.model.model_id}" if name else f"{agent.__class__.__name__} | {agent.model.model_id}",
        "type": agent.__class__.__name__,
        "description": getattr(agent, "description", ""),
        "authorized_imports": getattr(agent, "additional_authorized_imports", []),
        "tools": [
            {
                "name": tool_name,
                "description": getattr(tool, "description", str(tool)),
                "args": {
                    arg_name: {
                        "type": arg_info.get("type", "Any"),
                        "optional": arg_info.get("optional", False),
                        "description": arg_info.get("description", "")
                    }
                    for arg_name, arg_info in getattr(tool, "inputs", {}).items()
                }
            }
            for tool_name, tool in getattr(agent, "tools", {}).items()
        ],
        "managed_agents": [
            agent_to_dict(subagent, subname)
            for subname, subagent in getattr(agent, "managed_agents", {}).items()
        ]
    }


def MCPToolsVisualizer(mcp_client):
    tools = mcp_client.get_tools()

    def example_input_for_param(param_schema):
        param_type = param_schema.get("type", "string")
        if param_type == "string":
            return "example text"
        elif param_type == "integer":
            return 42
        elif param_type == "number":
            return 3.14
        elif param_type == "boolean":
            return True
        elif param_type == "array":
            return []
        elif param_type == "object":
            return {}
        else:
            return None

    def get_tool_summaries(tools):
        tool_summaries = []
        for tool in tools:
            example_inputs = {
                param_name: example_input_for_param(param_schema)
                for param_name, param_schema in tool.inputs.items()
            }
            tool_summary = {
                "name": tool.name,
                "description": tool.description,
                "inputs": tool.inputs,
                "example_inputs": example_inputs,
                "output_type": tool.output_type,
            }
            tool_summaries.append(tool_summary)
        return tool_summaries

    tool_summaries = get_tool_summaries(tools)

    def call_tool(tool_name, input_json):
        for tool in tools:
            if tool.name == tool_name:
                try:
                    inputs = json.loads(input_json)
                    start = time.time()
                    output = tool.forward(inputs)
                    latency = time.time() - start
                    return f"✅ Output: {output}\n⏱️ Latency: {latency:.3f} seconds"
                except Exception as e:
                    return f"❌ Error: {str(e)}"
        return "Tool not found."

    with gr.Blocks() as component:
        gr.Markdown(f"# MCP Server Info")
        # gr.Markdown(f"**Name:** {server_info.get('name', 'N/A')}")
        # gr.Markdown(f"**Version:** {server_info.get('version', 'N/A')}")
        # gr.Markdown(f"**Description:** {server_info.get('description', 'N/A')}")

        with gr.Accordion("Available Tools", open=True):
            for tool_summary in tool_summaries:
                with gr.Accordion(f"🛠️ {tool_summary['name']}", open=False):
                    gr.Markdown(f"**Description:** {tool_summary['description']}")
                    gr.Markdown(f"**Inputs:**\n```json\n{json.dumps(tool_summary['inputs'], indent=2)}\n```")
                    with gr.Row():
                        input_box = gr.Textbox(label="Tool Input (JSON)", lines=5, value=json.dumps(tool_summary['example_inputs'], indent=2))
                    with gr.Row():
                        call_button = gr.Button("Call Tool")
                    output_box = gr.Textbox(label="Tool Output", lines=5)

                    call_button.click(fn=call_tool, inputs=[gr.State(tool_summary['name']), input_box], outputs=[output_box])

    return component
