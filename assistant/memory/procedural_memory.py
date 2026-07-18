class ProceduralMemory:

    def __init__(self):

        self.skills = {}

    def register(self, name, tool):

        self.skills[name] = tool

    def get(self, name):

        return self.skills.get(name)