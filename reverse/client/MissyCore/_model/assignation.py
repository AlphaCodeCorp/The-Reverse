from .target import Target

class Assignation():

    def __init__(self, id: int):
        self.id = id
        self.secretaire
        self.animateur
        self.scribe
        self.gestionnaire

    def splitAssignations(self, assignation):

        for _assignation in assignation:

            if(_assignation[0] == "Animateur"):
                self.animateur = _assignation[1]
            elif(_assignation[0] == "Secretaire"):
                self.secretaire = _assignation[1]
            elif(_assignation[0] == "Scribe"):
                self.scribe = _assignation[1]
            elif(_assignation[0] == "Gestionnaire"):
                self.gestionnaire = _assignation[1]
