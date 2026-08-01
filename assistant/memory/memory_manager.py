from assistant.memory.working_memory import WorkingMemory
from assistant.memory.semantic_memory import SemanticMemory
from assistant.memory.session_context import SessionContext


class MemoryManager:

    def __init__(self):
        self.working = WorkingMemory()
        self.semantic = SemanticMemory()
        self.session_context = SessionContext()

    def set_context(self, key, value):
        self.session_context.set(key, value)

    def get_context(self, key, default=None):
        return self.session_context.get(key, default)

    def remove_context(self, key):
        self.session_context.remove(key)

    def clear_context(self):
        self.session_context.clear()

    def add_interaction(self, user: str, assistant: str):
        self.working.add("user", user)
        self.working.add("assistant", assistant)

    def get_recent_messages(self):
        return self.working.get()

    def remember(self, key, value):
        self.semantic.remember(key, value)

    def recall(self, key):
        return self.semantic.recall(key)

    def forget(self, key):
        return self.semantic.forget(key)