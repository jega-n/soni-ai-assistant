from assistant.memory.working_memory import WorkingMemory
from assistant.memory.episodic_memory import EpisodicMemory
from assistant.memory.semantic_memory import SemanticMemory
from assistant.memory.procedural_memory import ProceduralMemory
from assistant.memory.tool_cache import ToolCache
from assistant.memory.session_context import SessionContext


class MemoryManager:

    def __init__(self):

        self.working = WorkingMemory()

        self.episodic = EpisodicMemory()

        self.semantic = SemanticMemory()

        self.procedural = ProceduralMemory()

        self.cache = ToolCache()

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

        # Save conversation for prompt history
        self.working.add("user", user)
        self.working.add("assistant", assistant)

        # Save an episode
        self.episodic.add({
            "user": user,
            "assistant": assistant
        })

    def get_recent_messages(self):
        return self.working.get()

    def get_recent_events(self):
        return self.episodic.retrieve()

    def remember(self, key, value):
        self.semantic.remember(key, value)

    def recall(self, key):
        return self.semantic.recall(key)

    def forget(self, key):
        return self.semantic.forget(key)

    def register_skill(self, name, tool):
        self.procedural.register(name, tool)

    def get_skill(self, name):
        return self.procedural.get(name)