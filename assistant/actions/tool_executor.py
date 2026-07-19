from assistant.utils.logger import logger


class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name: str, **kwargs):

        tool = self.registry.get(tool_name)

        if tool is None:

            return {
                "success": False,
                "tool": tool_name,
                "tool_type": None,
                "result": None,
                "data": None,
                "response": None,
                "error": "Tool not found."
            }

        try:

            result = tool.execute(**kwargs)

            return {
                "success": result["success"],
                "tool": tool_name,
                "tool_type": tool.tool_type,
                "data": result["data"],
                "result": result,
                "response": result["response"],
                "error": None
            }

        except Exception as e:

            logger.exception(e)

            return {
                "success": False,
                "tool": tool_name,
                "tool_type": tool.tool_type,
                "result": None,
                "data": None,
                "response": None,
                "error": str(e)
            }