import os
import psutil
from datetime import datetime

from assistant.actions.base_tool import BaseTool, ToolType


class SystemInfoTool(BaseTool):

    name = "system_info"

    description = (
        "Reports a live system metric: CPU usage, memory usage, disk usage, "
        "battery status, the current time, the current date, or all of them together. "
        "Use this for any question about system stats or what time/date it is right now."
    )

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
                    "response": f"CPU usage is currently {cpu}%.",
                    "data": {
                        "cpu_percent": cpu
                    },
                    "llm": False
                }

            elif metric == "memory":

                memory = psutil.virtual_memory()

                memory_used = memory.used // (1024 ** 3)
                memory_total = memory.total // (1024 ** 3)

                return {
                    "success": True,
                    "response": (
                        f"Memory usage is {memory.percent}%. "
                        f"Using {memory_used} of {memory_total} GB."
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

                disk = psutil.disk_usage(
                    os.environ.get("SystemDrive", "C:") + "\\"
                )

                disk_used = disk.used // (1024 ** 3)
                disk_total = disk.total // (1024 ** 3)
                disk_free = disk.free // (1024 ** 3)

                return {
                    "success": True,
                    "response": (
                        f"Disk usage is {disk.percent}%. "
                        f"{disk_used} of {disk_total} GB are in use, "
                        f"with {disk_free} GB free."
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

                charging = (
                    "charging"
                    if battery.power_plugged
                    else "running on battery"
                )

                return {
                    "success": True,
                    "response": (
                        f"Battery is at {battery.percent}% and is {charging}."
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
                    "response": f"It's {now.strftime('%I:%M %p')}.",
                    "data": {
                        "time": now.strftime("%I:%M:%S %p")
                    },
                    "llm": False
                }

            elif metric == "date":

                now = datetime.now()

                return {
                    "success": True,
                    "response": (
                        f"Today is {now.strftime('%A, %d %B %Y')}."
                    ),
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
                        f"Today is {now.strftime('%A, %d %B %Y')}. "
                        f"It's {now.strftime('%I:%M %p')}."
                    ),
                    "data": {
                        "date": now.strftime("%A, %d %B %Y"),
                        "time": now.strftime("%I:%M:%S %p")
                    },
                    "llm": False
                }

            elif metric == "all":

                now = datetime.now()

                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()

                disk = psutil.disk_usage(
                    os.environ.get("SystemDrive", "C:") + "\\"
                )

                battery = psutil.sensors_battery()

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

                    "battery": (
                        None if battery is None else {
                            "percent": battery.percent,
                            "power_plugged": battery.power_plugged,
                            "seconds_left": battery.secsleft
                        }
                    ),

                    "date": now.strftime("%A, %d %B %Y"),
                    "time": now.strftime("%I:%M:%S %p")
                }

                battery_text = (
                    "Battery information isn't available."
                    if battery is None
                    else f"Battery is at {battery.percent}%."
                )

                response = (
                    f"CPU usage is {cpu}%, "
                    f"memory usage is {memory.percent}%, "
                    f"disk usage is {disk.percent}%. "
                    f"{battery_text}"
                )

                return {
                    "success": True,
                    "response": response,
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