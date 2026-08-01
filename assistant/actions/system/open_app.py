import os
import subprocess

from assistant.actions.base_tool import BaseTool, ToolType
from assistant.config.settings import APPLICATIONS


class OpenAppTool(BaseTool):

    name = "open_app"

    tool_type = ToolType.DETERMINISTIC

    parameters = {
        "query": "string"
    }

    APPS = APPLICATIONS

    def execute(self, query: str, **kwargs):

        application = query.lower().strip()

        if application in self.APPS:

            subprocess.Popen(self.APPS[application])

            return {
                "success": True,
                "response": f"Opened {application}.",
                "data": {
                    "application": application
                },
                "llm": False
            }

        if os.path.exists(application):

            subprocess.Popen(application)

            return {
                "success": True,
                "response": f"Opened {application}.",
                "data": {
                    "application": application
                }, 
                "llm": False
            }

        return {
            "success": False,
            "response": None,
            "data": None,
            "llm": False
        }