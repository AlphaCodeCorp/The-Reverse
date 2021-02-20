from .target import Target
from .assignation import Assignation
from reverse.core import utils
from discord.utils import get as disc_get
import datetime

class MissyCore():
    
    def __init__(self, ctx):
        self.channel = disc_get(ctx.guild.channels, name='austria')
        self.targetG1 = Target(1, utils.getRole(807261746758680609, ctx), self.channel, "G1"), 
        self.assigAnim = Assignation(1, self.targetG1, "Animateur")
        self.assigSecr = Assignation(2, self.targetG1, "Secretaire")

    def roll(self, date: datetime.date, target: Target):
        print("C'est ok")
