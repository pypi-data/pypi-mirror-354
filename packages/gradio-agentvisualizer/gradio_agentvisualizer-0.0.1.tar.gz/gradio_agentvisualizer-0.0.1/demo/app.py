
import gradio as gr
from gradio_agentvisualizer import AgentVisualizer, agent_to_dict, MCPToolsVisualizer

from custom_agent import manager_agent
from smolagents import MCPClient

smolagent_dict = agent_to_dict(manager_agent)
example = AgentVisualizer().example_value()


with gr.Blocks() as demo:
    with gr.Row():
        AgentVisualizer(label="Blank"),  # blank component
        AgentVisualizer(value=smolagent_dict, label="Populated"),  # populated component
if __name__ == "__main__":
    demo.launch()
