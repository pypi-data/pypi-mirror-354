# Gradio MCP Tool Visualizer

**Gradio MCP Tool Visualizer** is a visualizer for MCP tools. It allows developers and researchers to explore the structure of a mcp server by rendering tools and example input in an interactive and searchable list.

## Features

- Visualize mcp stucture
- Searchable list
- Visualize example components

## Usage

### Installation

```bash
pip install -r gradio-mcp-tools-visualizer
```

### Confugiration

```python
import gradio as gr
from gradio_mcp_tools_visualizer import mcp_tools_visualizer


server_parameters = {"url": "https://abidlabs-mcp-tools2.hf.space/gradio_api/mcp/sse", "transport": "sse"}  # <--- Your MCP server parameters

with gr.Tab("MCP Tool Visualizer"):
        mcp_tools_visualizer(
            value={
                'server_parameters': server_parameters
            },
        )
```

---
tags: [gradio-custom-component, ]
title: gradio_mcp_tools_visualizer
short_description: A gradio custom component
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---
