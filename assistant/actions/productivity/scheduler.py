from assistant.actions.base_tool import BaseTool, ToolType
from assistant.database.task_store import TaskStore


class SchedulerTool(BaseTool):

    name = "scheduler"

    description = (
        "Creates a time-based reminder (create_reminder), creates a to-do item "
        "with no fixed time (create_todo), lists scheduled tasks, or deletes a "
        "task by its task_id."
    )

    parameters = {
        "action": "create_reminder | create_todo | list | delete",
        "title": "string",
        "time": "string (optional)",
        "task_id": "integer (optional)"
    }

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

                if time is None:
                    return {
                        "success": False,
                        "response": "Reminder time is required.",
                        "data": None,
                        "llm": False
                    }

                reminder_title = "reminder" if title is None else title

                new_task_id = self._store.create_task(
                    task_type="reminder",
                    title=reminder_title,
                    time=time
                )

                return {
                    "success": True,
                    "response": "Reminder created successfully.",
                    "data": {
                        "task_id": new_task_id
                    },
                    "llm": False
                }

            elif action == "create_todo" or action == "create":

                todo_title = "todo" if title is None else title

                new_task_id = self._store.create_task(
                    task_type="todo",
                    title=todo_title
                )

                return {
                    "success": True,
                    "response": "Todo created successfully.",
                    "data": {
                        "task_id": new_task_id
                    },
                    "llm": False
                }

            elif action == "list":

                tasks = self._store.list_tasks()

                return {
                    "success": True,
                    "response": None,
                    "data": {
                        "tasks": tasks
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