from assistant.actions.tool_executor import ToolExecutor
from assistant.brain.llm import LLM
from assistant.brain.prompt_builder import PromptBuilder
from assistant.memory.memory_manager import MemoryManager
from assistant.memory.session_context import SessionContext


class ExecutionEngine:

    def __init__(self, tool_executor: ToolExecutor):

        self.executor = tool_executor
        self.llm = LLM()
        self.session = SessionContext()

        self.memory = MemoryManager()
        self.prompt_builder = PromptBuilder(self.memory)

    # --------------------------------------------------

    def execute(self, user_input: str, plan: dict):

        if plan["tool"] is None:

            prompt = self.prompt_builder.build(
            user_input=user_input,
            tool_data=None,
            session_context=self.session.all()
        )

            response = self.llm.ask(prompt)

            self.memory.add_interaction(
                user=user_input,
                assistant=response
            )

            return response

        result = self.executor.execute(
            plan["tool"],
            **plan["parameters"]
        )

        self._update_session(
            user_input=user_input,
            plan=plan,
            result=result
        )

        response = self._handle_tool_result(
            user_input,
            plan,
            result
        )

        self.memory.add_interaction(
            user=user_input,
            assistant=response
        )

        return response

    # --------------------------------------------------

    def _handle_tool_result(
        self,
        user_input,
        plan,
        result
    ):

        if not result["success"]:

            fallback = self._try_fallback(plan)

            if fallback is not None:

                self.session.set("last_response", fallback)
                return fallback

            response = result["response"] or "Operation failed."

            self.session.set("last_response", response)

            return response

        # Tool already produced a final response
        if result["response"] is not None:

            self.session.set("last_response", result["response"])

            return result["response"]

        # Tool returned structured data -> ask LLM
        prompt = self.prompt_builder.build(
            user_input=user_input,
            tool_data=result["data"],
            session_context=self.session.all()
        )

        response = self.llm.ask(prompt)

        self.session.set("last_response", response)

        return response

    # --------------------------------------------------

    def _try_fallback(self, plan):

        if plan["tool"] != "open_app":
            return None

        search = self.executor.execute(
            "file_search",
            query=plan["parameters"]["application"]
        )

        if not search["success"]:
            return None

        data = search["result"]["data"]

        if not data:
            return None

        if isinstance(data, list):
            path = data[0]["path"]
        else:
            path = data["path"]

        opened = self.executor.execute(
            "open_file",
            path=path
        )

        return opened["response"]
    
    def _update_session(self, user_input, plan, result):

        if not result["success"]:
            return

        self.session.set("last_user_input", user_input)
        self.session.set("last_tool", plan["tool"])
        self.session.set("last_parameters", plan["parameters"])

        if result["data"] is not None:
            self.session.set("last_data", result["data"])