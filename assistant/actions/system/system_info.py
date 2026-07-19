import psutil

from assistant.actions.base_tool import BaseTool, ToolType


class SystemInfoTool(BaseTool):

    name = "system_info"

    description = "Retrieve CPU, memory, disk and battery information."

    parameters = {
        "metric": "cpu | memory | disk | battery | all"
    }

    examples = [
        "What is my CPU usage?",
        "How much RAM is used?",
        "Show disk usage",
        "Battery percentage",
        "Show system information"
    ]

    tool_type = ToolType.DETERMINISTIC

    def execute(self, metric="all"):

        try:

            if metric == "cpu":

                data = {
                    "cpu_percent": psutil.cpu_percent(interval=1)
                }

            elif metric == "memory":

                memory = psutil.virtual_memory()

                data = {
                    "memory_total": memory.total,
                    "memory_used": memory.used,
                    "memory_available": memory.available,
                    "memory_percent": memory.percent
                }

            elif metric == "disk":

                disk = psutil.disk_usage("/")

                data = {
                    "disk_total": disk.total,
                    "disk_used": disk.used,
                    "disk_free": disk.free,
                    "disk_percent": disk.percent
                }

            elif metric == "battery":

                battery = psutil.sensors_battery()

                if battery is None:

                    return {
                        "success": False,
                        "response": "Battery information is not available.",
                        "data": None,
                        "llm": False
                    }

                data = {
                    "battery_percent": battery.percent,
                    "power_plugged": battery.power_plugged,
                    "seconds_left": battery.secsleft
                }

            elif metric == "all":

                memory = psutil.virtual_memory()
                disk = psutil.disk_usage("/")
                battery = psutil.sensors_battery()

                data = {
                    "cpu_percent": psutil.cpu_percent(interval=1),

                    "memory": {
                        "total": memory.total,
                        "used": memory.used,
                        "available": memory.available,
                        "percent": memory.percent
                    },

                    "disk": {
                        "total": disk.total,
                        "used": disk.used,
                        "free": disk.free,
                        "percent": disk.percent
                    },

                    "battery": None if battery is None else {
                        "percent": battery.percent,
                        "power_plugged": battery.power_plugged,
                        "seconds_left": battery.secsleft
                    }
                }

            else:

                return {
                    "success": False,
                    "response": f"Unsupported metric: {metric}",
                    "data": None,
                    "llm": False
                }

            return {
                "success": True,
                "response": None,
                "data": data,
                "llm": False
            }

        except Exception as e:

            return {
                "success": False,
                "response": f"Failed to retrieve system information: {str(e)}",
                "data": None,
                "llm": False
            }