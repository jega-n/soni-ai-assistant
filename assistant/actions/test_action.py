from assistant.actions.base_tool import BaseTool
from assistant.actions.registry import ToolRegistry
from assistant.actions.tool_executor import ToolExecutor


class HelloTool(BaseTool):
    name = "hello"
    description = "Test tool"

    def execute(self, **kwargs):
        return "Hello from tool!"


registry = ToolRegistry()
registry.register(HelloTool())

executor = ToolExecutor(registry)

result = executor.execute("hello")

print(result)