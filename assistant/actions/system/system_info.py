import psutil
from datetime import datetime
from assistant.actions.base_tool import BaseTool, ToolType


class SystemInfoTool(BaseTool):

    name = "system_info"

    parameters = {
        "metric": "cpu | memory | disk | battery | time | date | datetime | all"
    }

    tool_type = ToolType.DETERMINISTIC

    def execute(self, metric="all"):

        try:

            if metric == "cpu":

                cpu = psutil.cpu_percent(interval=1)

                return {
                    "success": True,
                    "response": f"Current CPU usage is {cpu}%.",
                    "data": {
                        "cpu_percent": cpu
                    },
                    "llm": False
                }

            elif metric == "memory":

                memory = psutil.virtual_memory()

                return {
                    "success": True,
                    "response": (
                        f"Memory usage is {memory.percent}%. "
                        f"Available memory is {memory.available // (1024**3)} GB."
                    ),
                    "data": {
                        "memory_total": memory.total,
                        "memory_used": memory.used,
                        "memory_available": memory.available,
                        "memory_percent": memory.percent
                    },
                    "llm": False
                }

            elif metric == "disk":

                disk = psutil.disk_usage("/")

                return {
                    "success": True,
                    "response": (
                        f"Disk usage is {disk.percent}%. "
                        f"Free space is {disk.free // (1024**3)} GB."
                    ),
                    "data": {
                        "disk_total": disk.total,
                        "disk_used": disk.used,
                        "disk_free": disk.free,
                        "disk_percent": disk.percent
                    },
                    "llm": False
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

                charging = "charging" if battery.power_plugged else "not charging"

                return {
                    "success": True,
                    "response": (
                        f"Battery is at {battery.percent}% and is currently {charging}."
                    ),
                    "data": {
                        "battery_percent": battery.percent,
                        "power_plugged": battery.power_plugged,
                        "seconds_left": battery.secsleft
                    },
                    "llm": False
                }

            elif metric == "time":

                now = datetime.now()

                return {
                    "success": True,
                    "response": f"The current time is {now.strftime('%I:%M:%S %p')}.",
                    "data": {
                        "time": now.strftime("%I:%M:%S %p")
                    },
                    "llm": False
                }

            elif metric == "date":

                now = datetime.now()

                return {
                    "success": True,
                    "response": f"Today is {now.strftime('%A, %d %B %Y')}.",
                    "data": {
                        "date": now.strftime("%A, %d %B %Y")
                    },
                    "llm": False
                }

            elif metric == "datetime":

                now = datetime.now()

                return {
                    "success": True,
                    "response": (
                        f"Today is {now.strftime('%A, %d %B %Y')} and the current time is "
                        f"{now.strftime('%I:%M:%S %p')}."
                    ),
                    "data": {
                        "date": now.strftime("%A, %d %B %Y"),
                        "time": now.strftime("%I:%M:%S %p")
                    },
                    "llm": False
                }

            elif metric == "all":

                now = datetime.now()

                memory = psutil.virtual_memory()
                disk = psutil.disk_usage("/")
                battery = psutil.sensors_battery()
                cpu = psutil.cpu_percent(interval=1)

                data = {
                    "cpu_percent": cpu,
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
                    },
                    "date": now.strftime("%A, %d %B %Y"),
                    "time": now.strftime("%I:%M:%S %p")
                }

                battery_text = (
                    "Battery information unavailable."
                    if battery is None
                    else f"Battery is {battery.percent}%."
                )

                return {
                    "success": True,
                    "response": (
                        f"CPU usage is {cpu}%. "
                        f"Memory usage is {memory.percent}%. "
                        f"Disk usage is {disk.percent}%. "
                        f"{battery_text} "
                        f"Today is {data['date']} and the current time is {data['time']}."
                    ),
                    "data": data,
                    "llm": False
                }

            else:

                return {
                    "success": False,
                    "response": f"Unsupported metric: {metric}",
                    "data": None,
                    "llm": False
                }

        except Exception as e:

            return {
                "success": False,
                "response": f"Failed to retrieve system information: {str(e)}",
                "data": None,
                "llm": False
            }