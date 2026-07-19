

from assistant.actions.base_tool import BaseTool, ToolType
from assistant.database.task_store import TaskStore


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

    _store = TaskStore()

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
                        "data": None,
                        "llm": False
                    }

                task_id = self._store.create_task(
                    task_type="reminder",
                    title=title,
                    time=time
                )

                return {
                    "success": True,
                    "response": "Reminder created successfully.",
                    "data": {
                        "task_id": task_id
                    },
                    "llm": False
                }

            elif action == "create_todo":

                if not title:
                    return {
                        "success": False,
                        "response": "Todo title is required.",
                        "data": None,
                        "llm": False
                    }

                task_id = self._store.create_task(
                    task_type="todo",
                    title=title
                )

                return {
                    "success": True,
                    "response": "Todo created successfully.",
                    "data": {
                        "task_id": task_id
                    },
                    "llm": False
                }

            elif action == "list":

                return {
                    "success": True,
                    "response": None,
                    "data": {
                        "tasks": self._store.list_tasks()
                    },
                    "llm": False
                }

            elif action == "delete":

                if task_id is None:
                    return {
                        "success": False,
                        "response": "Task ID is required.",
                        "data": None,
                        "llm": False
                    }

                deleted = self._store.delete_task(task_id)

                if not deleted:

                    return {
                        "success": False,
                        "response": "Task not found.",
                        "data": None,
                        "llm": False
                    }

                return {
                    "success": True,
                    "response": "Task deleted successfully.",
                    "data": {
                        "task_id": task_id
                    },
                    "llm": False
                }

            else:

                return {
                    "success": False,
                    "response": f"Unsupported action: {action}",
                    "data": None,
                    "llm": False
                }

        except Exception as e:

            return {
                "success": False,
                "response": str(e),
                "data": None,
                "llm": False
            }