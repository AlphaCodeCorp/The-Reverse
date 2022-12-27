from discord.ext import commands
from discord import Embed, Colour
import datetime
from reverse.core import utils
from reverse.core._service import SqliteService


class ReverseRoles(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = SqliteService()
	
	@commands.command()
	async def createRole(self, ctx, *args):
		guild = ctx.guild
		_kwargs, _args = utils.parse_args(args)
		if(guild):
			if(_kwargs["name"]):
				await guild.create_role(name=_kwargs["name"], colour=Colour.from_str(_kwargs["color"]))


	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		pass

def setup(bot):
	bot.add_cog(ReverseRoles(bot))
