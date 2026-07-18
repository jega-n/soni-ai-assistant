import os
import ollama
from assistant.brain.prompt_builder import PromptBuilder
from assistant.memory.memory_manager import MemoryManager
from assistant.utils.logger import logger
from assistant.config.settings import LLM_MODEL

class LLM:

    def __init__(self):

        self.model = LLM_MODEL

        self.memory = MemoryManager()

        self.prompt_builder = PromptBuilder(self.memory)

    def ask(self, user_input: str, tool_result=None):

        self.memory.working.add(
            "user",
            user_input
        )

        logger.info(f"User '{user_input}' added to working memory.")

        messages = self.prompt_builder.build(
            user_input=user_input,
            tool_result=tool_result
        )

        logger.info("Prompt built successfully.")

        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        answer = response["message"]["content"].strip()

        self.memory.working.add(
            "assistant",
            answer
        )

        logger.info(f"Assistant '{answer}' added to working memory.")

        return answer