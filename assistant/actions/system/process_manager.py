import psutil

from assistant.actions.base_tool import BaseTool, ToolType


class ProcessManagerTool(BaseTool):

    name = "process_manager"

    description = "List running processes and terminate processes."

    parameters = {
        "action": "list | terminate",
        "name": "string (optional)",
        "pid": "integer (optional)"
    }

    examples = [
        "Show running applications",
        "List running processes",
        "Close Notepad",
        "Terminate process 1234"
    ]

    tool_type = ToolType.DETERMINISTIC

    def execute(self, action, name=None, pid=None):

        try:

            if action == "list":

                processes = []

                for process in psutil.process_iter(
                    ["pid", "name", "status"]
                ):

                    try:

                        info = process.info

                        processes.append({
                            "pid": info["pid"],
                            "name": info["name"],
                            "status": info["status"]
                        })

                    except (
                        psutil.NoSuchProcess,
                        psutil.AccessDenied
                    ):
                        continue

                return {
                    "success": True,
                    "response": None,
                    "data": {
                        "processes": processes
                    }
                }


            elif action == "terminate":

                if pid is not None:

                    process = psutil.Process(pid)
                    process.terminate()

                    return {
                        "success": True,
                        "response": f"Process {pid} terminated.",
                        "data": {
                            "pid": pid
                        }
                    }


                if name:

                    terminated = []

                    for process in psutil.process_iter(
                        ["pid", "name"]
                    ):

                        try:

                            process_name = process.info["name"]
                            
                            if (
                                process_name
                                and name.lower() in process_name.lower()
                            ):

                                process.terminate()

                                terminated.append({
                                    "pid": process.info["pid"],
                                    "name": process.info["name"]
                                })

                        except (
                            psutil.NoSuchProcess,
                            psutil.AccessDenied
                        ):
                            continue

                    if not terminated:

                        return {
                            "success": False,
                            "response": f"No running process named '{name}' found.",
                            "data": None
                        }

                    return {
                        "success": True,
                        "response": f"Terminated {len(terminated)} process(es) named '{name}'.",
                        "data": {
                            "terminated": terminated
                        }
                    }


                return {
                    "success": False,
                    "response": "Provide either a process name or PID.",
                    "data": None
                }


            return {
                "success": False,
                "response": f"Unsupported action: {action}",
                "data": None
            }

        except psutil.NoSuchProcess:

            return {
                "success": False,
                "response": "Process not found.",
                "data": None
            }

        except psutil.AccessDenied:

            return {
                "success": False,
                "response": "Permission denied while accessing the process.",
                "data": None
            }

        except Exception as e:

            return {
                "success": False,
                "response": str(e),
                "data": None
            }