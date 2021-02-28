from .target import Target
from .assignation import Assignation
from .event import Event
from reverse.core import utils
from discord.utils import get as disc_get
from discord import Guild, Role, Embed
import datetime

class MissyCore():

    def __init__(self):
        self.list_targets = []
        self.target_id_count = 0

    def setup(self, guild: Guild, role: String, channel: String, name: String):
        # set up Target
        self.channel = guild.get_channel(int(channel[2:-1]))
        self.target_id_count = self.target_id_count + 1
        self.target = Target(self.target_Id, self.channel, name, int(role[3:-1]), guild)
        self.list_targets.append(self.target)

        # TODO : Save target in DB. Be carefull about target_Id

    # TODO : Create function to init MissyCore and get target in DB

    async def tirage(self, ctx, date: String, target: String):
        print("--------START------")
        print(self.listTargets)
        print("--------------------")
        print(self.listAssignations)
        print("---------END--------")

        # i do my best here, but i don't know how improve the readability 
        if(utils.valideDate(date)):
            for _target in self.listTargets:
                if(int(target[3:1]) == _target.role.id):
                    event = Event(datetime.date.today(), date, _target.target_Id)
                    await event.roll(date, _target)
        else:
            await ctx.send("Incorrect data format, should be DD-MM-YYYY")
