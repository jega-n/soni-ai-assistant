from datetime import datetime

from assistant.actions.base_tool import BaseTool, ToolType


class SchedulerTool(BaseTool):

    name = "scheduler"

    description = "Create, list and manage reminders and todo tasks."

    parameters = {
        "action": "create_reminder | create_todo | list | delete",
        "title": "string",
        "time": "string (optional)",
        "task_id": "integer (optional)"
    }

    examples = [
        "Remind me at 5 PM to call John",
        "Create a todo to study NLP",
        "Show my tasks",
        "Delete task 2"
    ]

    tool_type = ToolType.DETERMINISTIC

    # Temporary in-memory storage
    _tasks = []
    _next_id = 1

    def execute(
        self,
        action,
        title=None,
        time=None,
        task_id=None
    ):

        try:

            if action == "create_reminder":

                if not title:
                    return {
                        "success": False,
                        "response": "Reminder title is required.",
                        "data": None
                    }

                task = {
                    "id": SchedulerTool._next_id,
                    "type": "reminder",
                    "title": title,
                    "time": time,
                    "status": "pending",
                    "created_at": datetime.now().isoformat(),
                    "completed": False
                }

                SchedulerTool._tasks.append(task)
                SchedulerTool._next_id += 1

                return {
                    "success": True,
                    "response": "Reminder created successfully.",
                    "data": {
                        "task_id": task["id"]
                    }
                }

            elif action == "create_todo":

                if not title:
                    return {
                        "success": False,
                        "response": "Todo title is required.",
                        "data": None
                    }

                task = {
                    "id": SchedulerTool._next_id,
                    "type": "todo",
                    "title": title,
                    "time": None,
                    "status": "pending",
                    "created_at": datetime.now().isoformat(),
                    "completed": False
                }

                SchedulerTool._tasks.append(task)
                SchedulerTool._next_id += 1

                return {
                    "success": True,
                    "response": "Todo created successfully.",
                    "data": {
                        "task_id": task["id"]
                    }
                }

            elif action == "list":

                return {
                    "success": True,
                    "response": None,
                    "data": {
                        "tasks": SchedulerTool._tasks
                    }
                }

            elif action == "delete":

                if task_id is None:
                    return {
                        "success": False,
                        "response": "Task ID is required.",
                        "data": None
                    }

                for task in SchedulerTool._tasks:

                    if task["id"] == task_id:

                        SchedulerTool._tasks.remove(task)

                        return {
                            "success": True,
                            "response": "Task deleted successfully.",
                            "data": {
                                "task_id": task_id
                            }
                        }

                return {
                    "success": False,
                    "response": "Task not found.",
                    "data": None
                }

            else:

                return {
                    "success": False,
                    "response": f"Unsupported action: {action}",
                    "data": None
                }

        except Exception as e:

            return {
                "success": False,
                "response": str(e),
                "data": None
            }