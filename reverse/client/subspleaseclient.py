from discord.ext import commands
from discord import Embed
import datetime
from functools import wraps

from reverse.core._service.subsplease import *
from reverse.core._service import TaskService
from reverse.core._models import Context
from reverse.core import utils

class SubspleaseClient(commands.Cog):

	def __init__(self, bot) -> None:
		self.bot = bot
		self.env = utils.load_backend().get("subsplease", {})

		self.s = Subsplease()
		
	def _process_schedule_today(self, data, guild) -> Embed:
		_schedule = json.loads(data)
		_episode = _schedule.get("schedule", [])
		_guild = guild

		_embed = Embed(title="Sorties du jour", color=0xe80005, timestamp=datetime.datetime.today())

		_emote = {
			"default": ["<:red_circle:1047568178391298128>", "<:green_circle:1047567792007819276>"],
			"217327494519324682": ["<:Sacrezar:499935992740839434>", "<:Valou2:946414196856332319>"]
		}
		
		if(str(_guild) in _emote and self.env.get("modified_emote", False) != "0"):
			_choose = _emote.get(str(_guild), None)
		else:
			_choose = _emote.get("default")

		if(len(_episode) > 0):
			for e in _episode:
				_name = e.get("title", "Unknown")
				_page = e.get("page", "Empty")
				_hour = e.get("time", "Unknown")

				if(e.get("aired", False) != False):
					_value = f"[{_hour}]\tDiffusion: {_choose[1]}\thttps://animixplay.to/v1/{_page}"
				else:
					_value = f"[{_hour}]\tDiffusion: {_choose[0]}\thttps://animixplay.to/v1/{_page}"
				_embed.add_field(name=_name, value=_value, inline=False)
		else:
			_embed.add_field(name="Aucune sortie", value="Un jour sans anime. Cringe", inline=False)
		_embed.set_footer(text=f"The Reverse")

		return _embed

	
	@commands.command(aliases=["opd", "la"])
	async def OpenYourDoor(self, ctx):
		data = await self.s.planning_anime()
		_guild = "0"
		if(hasattr(ctx.guild, "id")):
			_guild = ctx.guild.id
		
		embed = self._process_schedule_today(data, _guild)
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(SubspleaseClient(bot))