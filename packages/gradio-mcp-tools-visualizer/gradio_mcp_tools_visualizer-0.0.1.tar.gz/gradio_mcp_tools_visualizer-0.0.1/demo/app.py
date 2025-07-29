import gradio as gr
from gradio_mcp_tools_visualizer import mcp_tools_visualizer
from smolagents import MCPClient

server_parameters = {"url": "http://huggingface.co/mcp/", "transport": "streamable-http"}
with gr.Blocks() as demo:
    gr.Markdown("# MCP Tools Visualizer 🚀")
    mcp_tools_visualizer(
        value={
            'server_parameters': server_parameters
        },
    )

if __name__ == "__main__":
    demo.launch()



# import gradio as gr
# from gradio_mcp_tools_visualizer import mcp_tools_visualizer


# with gr.Blocks() as demo:
#     gr.Markdown("# Change the value (keep it JSON) and the front-end will update automatically.")
#     mcp_tools_visualizer(value={"message": "Hello from Gradio!"}, label="Static")


# if __name__ == "__main__":
#     demo.launch()