from .target import Target
from .assignation import Assignation
from reverse.core import utils
from discord.utils import get as disc_get
from discord import Guild
import datetime

class MissyCore():

    def __init__(self, guild: Guild):
        self.channel = disc_get(guild.channels, name='austria')
        self.role = utils.getRole(807261746758680609, guild)
        self.targetG1 = Target(1, self.channel, "G1", self.role, guild)
        #self.assigAnim = Assignation(1, self.targetG1, "Animateur")
        #self.assigSecr = Assignation(2, self.targetG1, "Secretaire")

    def roll(self, date: datetime.date, target: Target):
        print("C'est ok")
        print(self.channel)
        print(self.role)
        print(self.targetG1)
