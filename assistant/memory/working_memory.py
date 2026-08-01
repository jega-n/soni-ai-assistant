class WorkingMemory:

    def __init__(self, limit=10):
        self.limit = limit
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        while len(self.messages) > self.limit:
            self.messages.pop(0)

    def get(self):
        return list(self.messages)

    def clear(self):
        self.messages.clear()