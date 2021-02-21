from .target import Target
import random

class Assignation():
    
    def __init__(self, id: int, target: Target, name: str):
        self.id = id
        self.target = target
        self.name = name

    def getLastXTirages(self):
        # TODO
        return ["Jean", "Paul"]

    def clearTirage(self, users: list, lastTirage: list):
        # TODO
        return ["Jean", "Paul", "Maurice", "Alain", "Bob", "Thomas"]

    def roll(self, users: list):
        return random.choice(users)