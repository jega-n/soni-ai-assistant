class ToolCache:

    def __init__(self):

        self.cache = {}

    def save(self, key, value):

        self.cache[key] = value

    def get(self, key):

        return self.cache.get(key)