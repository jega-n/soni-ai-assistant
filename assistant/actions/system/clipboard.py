import pyperclip

from assistant.actions.base_tool import BaseTool, ToolType


class ClipboardTool(BaseTool):

    name = "clipboard"

    parameters = {
        "action": "read | copy",
        "text": "string (required for copy)"
    }

    tool_type = ToolType.DETERMINISTIC

    def execute(self, action, text=None):

        try:

            if action == "read":

                content = pyperclip.paste()

                if not content.strip():
                    return {
                        "success": True,
                        "response": "Your clipboard is empty.",
                        "data": {
                            "clipboard_text": ""
                        },
                        "llm": False
                    }

                return {
                    "success": True,
                    "response": f"Your clipboard contains: {content}",
                    "data": {
                        "clipboard_text": content
                    },
                    "llm": False
                }

            elif action == "copy":

                if not text:
                    return {
                        "success": False,
                        "response": "No text provided to copy.",
                        "data": None,
                        "llm": False
                    }

                pyperclip.copy(text)

                return {
                    "success": True,
                    "response": "Text copied to the clipboard.",
                    "data": {
                        "copied_text": text
                    },
                    "llm": False
                }

            else:

                return {
                    "success": False,
                    "response": f"Unsupported clipboard action: {action}",
                    "data": None,
                    "llm": False
                }

        except Exception as e:

            return {
                "success": False,
                "response": f"Clipboard operation failed: {str(e)}",
                "data": None,
                "llm": False
            }