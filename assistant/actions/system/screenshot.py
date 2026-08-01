from pathlib import Path
from datetime import datetime

import mss

from assistant.actions.base_tool import BaseTool, ToolType


class ScreenshotTool(BaseTool):

    name = "take_screenshot"

    description = "Captures the current screen and saves it as an image file. Takes no parameters."

    parameters = {}


    tool_type = ToolType.DETERMINISTIC

    def execute(self, **kwargs):

        folder = Path("screenshots")
        folder.mkdir(exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"

        path = folder / filename

        with mss.mss() as sct:
            sct.shot(output=str(path))

        return {
            "success": True,
            "response": f"Screenshot saved to {path}",
            "data": {
                "path": str(path)
            },
            "llm": False
        }