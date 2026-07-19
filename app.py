from assistant.utils.logger import logger
from assistant.config import settings

from assistant.brain.llm_planner import LLMPlanner
from assistant.actions.registry import ToolRegistry
from assistant.actions.tool_executor import ToolExecutor

from assistant.actions.system.clipboard import ClipboardTool
from assistant.actions.system.system_info import SystemInfoTool
from assistant.actions.system.process_manager import ProcessManagerTool
from assistant.actions.productivity.scheduler import SchedulerTool
from assistant.actions.system.screenshot import ScreenshotTool
from assistant.actions.system.open_app import OpenAppTool
from assistant.actions.files.file_search import FileSearchTool
from assistant.actions.files.open_file import OpenFileTool

from assistant.core.execution_engine import ExecutionEngine
from assistant.brain.llm import LLM
from assistant.speech.voice_loop import VoiceLoop


class Assistant:

    def __init__(self):

        self.name = settings.ASSISTANT_NAME
        self.version = settings.VERSION

        self.llm = LLM()
        self.registry = ToolRegistry()
        self.voice = VoiceLoop()

        self.registry.register(ScreenshotTool())
        self.registry.register(OpenAppTool())
        self.registry.register(FileSearchTool())
        self.registry.register(OpenFileTool())
        self.registry.register(ClipboardTool())
        self.registry.register(SystemInfoTool())
        self.registry.register(ProcessManagerTool())
        self.registry.register(SchedulerTool())

        executor = ToolExecutor(self.registry)
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

        if hasattr(self, "voice"):
            self.voice.wake.close()

        logger.info("Assistant shutting down.")
        print("Goodbye!")

    def run(self):

            while True:

                user_input = self.voice.wait_for_command()

                if not user_input:
                    continue

                print(f"\nYou: {user_input}")

                if user_input.lower() in ("exit", "quit"):
                    break

                plan = self.planner.plan(user_input)
                print("PLAN:", plan)

                response = self.engine.execute(
                    user_input=user_input,
                    plan=plan
                )

                print("RESPONSE:", response)

                print(f"Soni: {response}")

                self.voice.speak(response)

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