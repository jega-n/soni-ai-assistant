import pyperclip

from assistant.actions.base_tool import BaseTool, ToolType


class ClipboardTool(BaseTool):

    name = "clipboard"

    description = "Read or copy text from/to system clipboard."

    parameters = {
        "action": "read | copy",
        "text": "string (required for copy)"
    }

    examples = [
        "Read my clipboard",
        "Copy this text to clipboard"
    ]

    tool_type = ToolType.DETERMINISTIC


    def execute(self, action, text=None):

        try:

            if action == "read":

                content = pyperclip.paste()

                return {
                    "success": True,
                    "response": None,
                    "data": {
                        "clipboard_text": content
                    }
                }


            elif action == "copy":

                if not text:
                    return {
                        "success": False,
                        "response": "No text provided to copy.",
                        "data": None
                    }


                pyperclip.copy(text)

                return {
                    "success": True,
                    "response": "Text copied to clipboard.",
                    "data": {
                        "copied_text": text
                    }
                }


            else:

                return {
                    "success": False,
                    "response": f"Unsupported clipboard action: {action}",
                    "data": None
                }


        except Exception as e:

            return {
                "success": False,
                "response": f"Clipboard operation failed: {str(e)}",
                "data": None
            }