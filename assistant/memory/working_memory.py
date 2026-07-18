from assistant.database.conversation_store import ConversationStore


class WorkingMemory:

    def __init__(self, limit=10):

        self.limit = limit
        self.store = ConversationStore()


    def add(self, role, content):

        self.store.save_message(
            role,
            content
        )


    def get(self):

        return self.store.get_recent_messages(
            self.limit
        )


    def clear(self):

        self.store.clear()