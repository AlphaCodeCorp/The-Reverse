import datetime
from reverse.client.MissyCore._model import target, assignagtion

class MissyCore():
    
    def __init__(self, ctx):
        self.channel = discord.utils.get(ctx.guild.channels, name='austria')
        self.targetG1 = target.Target(1, utils.getRole(807261746758680609, ctx), self.channel, "G1"), 
        self.assigAnim = assignagtion.Assignation(1, self.targetG1, "Animateur")
        self.assigSecr = assignagtion.Assignation(2, self.targetG1, "Secretaire")

    def roll(self, date: datetime.date, target: target.Target):
        print("C'est ok")
