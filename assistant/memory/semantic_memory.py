class SemanticMemory:

    def __init__(self):

        self.knowledge = {}

    def remember(self, key, value):

        self.knowledge[key] = value

    def recall(self, key):

        return self.knowledge.get(key)