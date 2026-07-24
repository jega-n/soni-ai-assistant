from pathlib import Path

from assistant.actions.base_tool import BaseTool, ToolType
from assistant.actions.files.file_search import FileSearchTool
from assistant.config.settings import SUPPORTED_TEXT_FILES


class FileReaderTool(BaseTool):

    name = "read_file"

    planner_visible = True

    tool_type = ToolType.REASONING

    parameters = {
        "query": "string"
    }

    def __init__(self):
        self.search_tool = FileSearchTool()

    def execute(self, query: str, **kwargs):

        search = self.search_tool.execute(query=query)

        if not search["success"]:
            return search

        path = search["data"]["path"]

        file = Path(path)

        if file.suffix.lower() not in SUPPORTED_TEXT_FILES:
            return {
                "success": False,
                "response": f"{file.suffix} files are not supported yet.",
                "data": None,
                "llm": False
            }

        try:

            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            return {
                "success": True,
                "response": None,
                "data": {
                    "name": file.name,
                    "path": str(file),
                    "content": content
                },
                "llm": True
            }

        except Exception as e:

            return {
                "success": False,
                "response": str(e),
                "data": None,
                "llm": False
            }