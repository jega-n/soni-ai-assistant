class EpisodicMemory:

    def __init__(self):
        self.events = []

    def add(self, event):

        self.events.append(event)

    def retrieve(self):

        return self.events[-10:]