from collections import deque

class WorkingMemory:

    def __init__(self, limit=10):
        self.messages = deque(maxlen=limit)

    def add(self, role, content):

        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )

    def get(self):
        return list(self.messages)

    def clear(self):
        self.messages.clear()