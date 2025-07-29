import json
import time

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from gradio.components.base import Component
from gradio.components import Timer
from gradio.events import Events
from gradio.i18n import I18nData

from smolagents import MCPClient

# if TYPE_CHECKING:
#     print('type')
#     from gradio.components import Timer


class mcp_tools_visualizer(Component):

    EVENTS = [Events.input]

    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        label: str | I18nData | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool = False,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = "value",
        min_height: int | None = None,
        max_height: int | None = None,
        container: bool = False,
        padding: bool = True,
    ):
        self.min_height = min_height
        self.max_height = max_height
        self.padding = padding
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
            value=value,
            container=container,
        )

    def preprocess(self, payload):
        """
        Payload from frontend: { "action": "call_tool", "tool_name": str, "inputs": dict, "server_parameters": dict }
        """
        return {payload}

    def postprocess(self, value):
        """
        Frontend will receive initial data: { server_info, tool_summaries }
        """
        server_parameters = value.get("server_parameters")
        mcp_client = MCPClient(server_parameters)

        tool_summaries = self.get_tool_summaries(mcp_client.get_tools())
        return {
            "server_parameters": server_parameters,
            # "server_info": server_info,
            "tool_summaries": tool_summaries
        }

    def example_payload(self):
        return {
            "action": "call_tool",
            "tool_name": "example_tool",
            "inputs": {"param": "value"},
            "server_parameters": {"url": "http://huggingface.co/mcp/", "transport": "streamable-http"},
        }

    def example_value(self):
        return {
            "server_parameters": {"url": "http://huggingface.co/mcp/", "transport": "streamable-http"},
            "server_info": {},
            "tool_summaries": []
        }

    def api_info(self):
        return {"type": {}, "description": "any valid json"}

    def example_input_for_param(self, param_schema):
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

    def get_tool_summaries(self, tools):
            tool_summaries = []
            for tool in tools:
                example_inputs = {
                    param_name: self.example_input_for_param(param_schema)
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