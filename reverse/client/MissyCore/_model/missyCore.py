from .target import Target
from .assignation import Assignation
from .event import Event
from reverse.core import utils
from discord.utils import get as disc_get
from discord import Guild, Role, Embed
import datetime

class MissyCore():

    def __init__(self):
        self.listTargets = []
        self.listAssignations = []
        self.idAssi = 0

    def setup(self, guild: Guild, role: String, channel: String, name: String):
        # set up Target
        self.channel = guild.get_channel(int(channel[2:-1]))
        self.target = Target(1, self.channel, name, int(role[3:-1]), guild)
        self.listTargets.append(self.target)

        # Set up Assignations for Target
        self.idAssi = self.idAssi + 1
        self.listAssignations.append(Assignation(self.idAssi, self.target, "Animateur"))
        self.idAssi = self.idAssi + 1
        self.listAssignations.append(Assignation(self.idAssi, self.target, "Secretaire"))
        self.idAssi = self.idAssi + 1
        self.listAssignations.append(Assignation(self.idAssi, self.target, "Scribe"))
        self.idAssi = self.idAssi + 1
        self.listAssignations.append(Assignation(self.idAssi, self.target, "Gestionnaire"))