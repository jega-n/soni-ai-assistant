from assistant.brain.prompts import SYSTEM_PROMPT
import json



class PromptBuilder:

    def __init__(self, memory_manager):
        self.memory = memory_manager

    def build(
        self,
        user_input: str,
        tool_data=None,
        session_context=None
    ):

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Working Memory
        messages.extend(
            self.memory.working.get()
        )

        # Semantic Memory
        facts = self.memory.semantic.store.list_facts()

        for fact in facts:

            messages.append({
                "role": "system",
                "content": f"{fact['key']}: {fact['value']}"
            })

        # Session Context
        if session_context:

            messages.append({
                "role": "system",
                "content": (
                    "Current session context.\n"
                    "Use it to resolve references like "
                    "'it', 'that', 'them', 'the previous one'.\n\n"
                    f"{json.dumps(session_context, indent=2, ensure_ascii=False)}"
                )
            })

        # Tool Context
        if tool_data is not None:

            messages.append({
                "role": "system",
                "content": (
                    "The following structured data was produced by a trusted Python tool.\n"
                    "Treat this data as factual.\n\n"
                    f"{json.dumps(tool_data, indent=2, ensure_ascii=False)}"
                )
            })

        # Current User Message
        messages.append({
            "role": "user",
            "content": user_input
        })

        return messages