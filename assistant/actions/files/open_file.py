import os

from assistant.actions.base_tool import BaseTool, ToolType


class OpenFileTool(BaseTool):

    name = "open_file"

    description = "Open a local file using its default application."

    tool_type = ToolType.DETERMINISTIC

    parameters = {
        "path": "string"
    }

    examples = [
        "Open resume.pdf",
        "Open README.md",
        "Open report.docx",
        "Open notes.txt",
        "Open presentation.pptx"
    ]

    def execute(
        self,
        path: str,
        **kwargs
    ):

        if not os.path.exists(path):

            return {
                "success": False,
                "response": "File not found.",
                "data": None,
                "llm": False
            }

        try:

            os.startfile(path)

            return {
                "success": True,
                "response": "Opened the file.",
                "data": {
                    "path": path
                },
                "llm": False
            }

        except Exception:

            return {
                "success": False,
                "response": "Unable to open the file.",
                "data": None,
                "llm": False
            }