# Gradio AI Agent Visualizer

**Gradio AI Agent Visualizer** is a visualizer for ai agents. It allows developers and researchers to explore the structure of your AI agents by rendering name, description, tools, models and managed agents,  in an intuitive and expandable UI.


## Features

- Visualize agent structure
- Expand/collapse nested tool
- Ability to pass a dict to the component (Flexability if you don't use smolagents)
- Automatic agent to dict helper function

## Usage

### Installation

```bash
pip install -r gradio-agentvisualizer
```

### Confugiration

```python
import gradio as gr
from gradio_agentvisualizer import AgentVisualizer, agent_to_dict

from demo_agents.custom_agent import manager_agent  # <--- Your custom smolagent

smolagent_dict = agent_to_dict(manager_agent)  # <--- Returns a dict of your agent that you can pass into the component

with gr.Blocks() as demo:
    with gr.Tab("Agent Visualizer"):
        AgentVisualizer(value=smolagent_dict)
```

---
tags: [gradio-custom-component, HTML]
title: gradio_agentvisualizer
short_description: A gradio custom component
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

