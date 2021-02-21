from .target import Target
from .assignation import Assignation
from .event import Event
from reverse.core import utils
from discord.utils import get as disc_get
from discord import Guild, Role
import datetime

class MissyCore():

    def __init__(self):
        self.listTargets = []
        self.listAssignations = []
        self.idAssi = 0

    def initialisation(self, guild: Guild, _kwargs):

        # set up Target
        self.channel = disc_get(guild.channels, name=_kwargs["channel"])
        self.target = Target(1, self.channel, _kwargs["name"], int(_kwargs["role"][3:-1]), guild)
        self.listTargets.append(self.target)

        # Set up Assignations for Target
        self.idAssi = self.idAssi + 1
        self.listAssignations.append(Assignation(self.idAssi, self.target, "Animateur"))
        self.idAssi = self.idAssi + 1
        self.listAssignations.append(Assignation(self.idAssi, self.target, "Secretaire"))
        self.idAssi = self.idAssi + 1
        self.listAssignations.append(Assignation(self.idAssi, self.target, "Scribe"))

    def roll(self, date: datetime.date, target: Target):
        print("--------START------")
        print(self.listTargets)
        print("--------------------")
        print(self.listAssignations)
        print("---------END--------")

        membersPick = []

        # Pour la target
        listMembers = target.getAllMembers()

        # Comparer la liste des utilisateurs de ce role sur le serveur 
        # à la liste des utilisateurs dans la base de données
        if target.compare(listMembers):
            for assignation in self.listAssignations:
                if assignation.target == target:

                    XlastTirage = assignation.getLastXTirages()
                    users = assignation.clearTirage(listMembers, XlastTirage)
                    user = assignation.roll(users)
                    membersPick.append([assignation.name, user])

            print(membersPick)
            