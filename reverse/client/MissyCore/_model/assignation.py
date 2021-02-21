from .target import Target

class Assignation():
    
    def __init__(self, id: int, target: Target, name: str):
        self.id = id
        self.target = target
        self.name = name

    def getLastXTirages(self):
        return ["Jean", "Paul"]

    def clearTirage(self, users: list, lastTirage: list):
        return ["Jean", "Paul"]

    def roll(self, users: list):
        return "Paul"