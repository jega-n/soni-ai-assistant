from copy import deepcopy


class SessionContext:
    """
    Stores temporary execution state for the current session.

    This is NOT long-term memory.

    Examples:
        - Last search results
        - Current document
        - Current webpage
        - Last calculator result
        - Active task
    """

    def __init__(self):
        self.clear()

    def set(self, key: str, value):
        self._context[key] = deepcopy(value)

    def get(self, key: str, default=None):
        return deepcopy(self._context.get(key, default))

    def exists(self, key: str):
        return key in self._context

    def remove(self, key: str):
        self._context.pop(key, None)

    def clear(self):
        self._context = {}

    def all(self):
        return deepcopy(self._context)