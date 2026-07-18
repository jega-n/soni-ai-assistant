from assistant.database.fact_store import FactStore


class SemanticMemory:

    def __init__(self):

        self.store = FactStore()


    def remember(self, key, value):

        self.store.save_fact(
            key,
            value
        )


    def recall(self, key):

        return self.store.get_fact(
            key
        )


    def forget(self, key):

        return self.store.delete_fact(
            key
        )


    def all(self):

        return self.store.list_facts()