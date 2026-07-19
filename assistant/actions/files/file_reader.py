from pathlib import Path

from assistant.actions.base_tool import BaseTool, ToolType
from assistant.config.settings import SUPPORTED_TEXT_FILES


class FileReaderTool(BaseTool):

    name = "file_reader"
    description = "Read text files."
    tool_type = ToolType.REASONING
    parameters = {
        "application": "string"
    }

    examples = [
        "Open Notepad",
        "Launch Calculator",
        "Start Chrome"
    ]

    def execute(self, path: str, **kwargs):

        file = Path(path)

        if not file.exists():
            return {
                "success": False,
                "response": "File not found.",
                "data": None,
                "llm": True
            }

        if file.suffix.lower() not in SUPPORTED_TEXT_FILES:
            return {
                "success": False,
                "response": f"{file.suffix} is not supported yet.",
                "data": None,
                "llm": True
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
                "llm": True
            }