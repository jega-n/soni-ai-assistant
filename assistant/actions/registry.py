from typing import Dict

from assistant.actions.base_tool import BaseTool


class ToolRegistry:

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def unregister(self, tool_name: str):
        self._tools.pop(tool_name, None)

    def get(self, tool_name: str):
        return self._tools.get(tool_name)

    def exists(self, tool_name: str):
        return tool_name in self._tools

    def list_tools(self):
        return list(self._tools.keys())

    def planner_tools(self):

        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
                "examples": tool.examples,
            }
            for tool in self._tools.values()
        ]