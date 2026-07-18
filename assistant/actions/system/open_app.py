import os
import subprocess

from assistant.actions.base_tool import BaseTool, ToolType
from assistant.config.settings import APPLICATIONS


class OpenAppTool(BaseTool):

    name = "open_app"

    description = "Open an installed desktop application."

    tool_type = ToolType.DETERMINISTIC

    parameters = {
        "application": "string"
    }

    examples = [
        "Open Notepad",
        "Launch Calculator",
        "Start Chrome"
    ]

    APPS = APPLICATIONS

    def execute(self, application: str, **kwargs):

        application = application.lower().strip()

        if application in self.APPS:

            subprocess.Popen(self.APPS[application])

            return {
                "success": True,
                "response": f"Opened {application}.",
                "data": {
                    "application": application
                }
            }

        if os.path.exists(application):

            subprocess.Popen(application)

            return {
                "success": True,
                "response": "Opened application.",
                "data": {
                    "application": application
                }
            }

        return {
            "success": False,
            "response": None,
            "data": None
        }