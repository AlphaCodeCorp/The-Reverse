from .target import Target

class Assignation():

    def __init__(self, id: int):
        self.id = id
        
        # Data like : [[animateur: Bob],[secretaire: Bob],[scribe: Bob],[gestionnaire: Bob]]
        self.assignationByRole