from assistant.actions.registry import ToolRegistry
from assistant.actions.tool_executor import ToolExecutor
from assistant.actions.system.open_app import OpenAppTool


registry = ToolRegistry()
registry.register(OpenAppTool())

executor = ToolExecutor(registry)

result = executor.execute(
    "open_app",
    application="notepad"
)

print(result)