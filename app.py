from actions.system.screenshot import ScreenshotTool
from assistant.utils.logger import logger
from assistant.config import settings

from assistant.brain.llm_planner import LLMPlanner
from assistant.actions.registry import ToolRegistry
from assistant.actions.tool_executor import ToolExecutor
from assistant.actions.system.clipboard import ClipboardTool
from assistant.actions.system.system_info import SystemInfoTool
from assistant.actions.system.process_manager import ProcessManagerTool
from assistant.actions.productivity.scheduler import SchedulerTool

from assistant.actions.system.open_app import OpenAppTool
from assistant.actions.files.file_search import FileSearchTool
from assistant.actions.files.open_file import OpenFileTool

from assistant.core.execution_engine import ExecutionEngine
from brain.llm import LLM


class Assistant:

    def __init__(self):

        self.name = settings.ASSISTANT_NAME
        self.version = settings.VERSION

        self.llm = LLM()
        registry = ToolRegistry()

        registry.register(ScreenshotTool())
        registry.register(OpenAppTool())
        registry.register(FileSearchTool())
        registry.register(OpenFileTool())
        registry.register(ClipboardTool())
        registry.register(SystemInfoTool())
        registry.register(ProcessManagerTool())
        registry.register(SchedulerTool())

        executor = ToolExecutor(registry)
        self.planner = LLMPlanner(
            self.llm,
            self.registry
        )
        self.engine = ExecutionEngine(executor)

    def start(self):

        logger.info(f"{self.name} v{self.version} started.")

        print("=" * 50)
        print(f"Welcome to {self.name}")
        print(f"Version : {self.version}")
        print("=" * 50)

    def shutdown(self):

        logger.info("Assistant shutting down.")
        print("Goodbye!")

    def run(self):

        while True:

            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                break

            plan = self.planner.plan(user_input)

            if plan["tool"]:

                tool_result = self.executor.execute(
                    plan["tool"],
                    **plan["parameters"]
                )

                if tool_result["response"]:
                    print(f"Soni: {tool_result['response']}")
                    continue

                prompt = self.prompt_builder.build(
                    user_input=user_input,
                    tool_data=tool_result["data"]
                )

            else:

                prompt = self.prompt_builder.build(
                    user_input=user_input
                )

            response = self.llm.generate(prompt)

            print(f"Soni: {response}")

def main():

    assistant = Assistant()

    try:

        assistant.start()
        assistant.run()

    except KeyboardInterrupt:

        logger.warning("Interrupted by user.")

    except Exception as e:

        logger.exception(e)
        print(e)

    finally:

        assistant.shutdown()


if __name__ == "__main__":
    main()