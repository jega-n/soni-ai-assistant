import ollama

from assistant.config.settings import (
    CHAT_MODEL,
    PLANNER_MODEL,
    PLANNER_OPTIONS
)


class LLM:

    def __init__(self):

        self.chat_model = CHAT_MODEL
        self.planner_model = CHAT_MODEL

    # --------------------------------------------------

    def chat(self, messages: list[dict]) -> str:

        response = ollama.chat(
            model=self.chat_model,
            messages=messages
        )

        return response["message"]["content"].strip()

    # --------------------------------------------------

    def plan(self, messages: list[dict]) -> str:

        response = ollama.chat(
            model=self.planner_model,
            messages=messages,
            options=PLANNER_OPTIONS
        )

        return response["message"]["content"].strip()