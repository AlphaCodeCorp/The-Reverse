from .target import Target
from .event import Event
from reverse.core import utils
from discord.utils import get as disc_get
from discord import Guild, Role, Embed
import datetime

class MissyCore():

    def __init__(self):
        self.list_targets = []
        self.target_id_count = 0

    def setup(self, guild: Guild, role: str, channel: str, name: str):
        '''set up Target'''
        self.channel = guild.get_channel(int(channel[2:-1]))
        self.target_id_count = self.target_id_count + 1
        self.target = Target(123, self.channel, name, int(role[3:-1]), guild)
        self.list_targets.append(self.target)

        # TODO : Save target in DB. Be carefull about target_Id

    # TODO : Create function to init MissyCore and get target in DB

    async def tirage(self, ctx, date: str, target: int):
        _isDate = utils.valideDate(date)
        if(_isDate):
            """List all target to process"""
            for _target in self.list_targets:
                if(target == _target.role.id):
                    event = Event(utils.now(), date, _target.id)
                    """TODO : Information log"""
                    await event.roll(date, _target)
        else:
            """TODO : Warning log"""
            await ctx.send("Incorrect data format, should be DD-MM-YYYY")
