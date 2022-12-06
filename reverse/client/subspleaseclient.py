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

	def _process_latest_release(self, data, guild, ctx):
		_latest = json.loads(data)
		_guild = guild

		_embed = Embed(title="Sorties du jour", color=0xe80005, timestamp=datetime.datetime.today())

		if(len(_latest) > 0):
			for e in _latest:
				_e = _latest.get(e, {})
				if(_e.get("time", "Unknown") != "New"):
					break
				
				_name = e
				_page = _e.get("page", "Empty")
				_hour = _e.get("release_date", "Unknown")
				_eps = _e.get("episode", "00")
				_downloads = _e.get("downloads", [])

				""" _n = ""
				for d in _downloads:
					_d = d.get("res", "Unknown")
					_url = d.get("magnet", "Unknown")
					_n = _n + f"\n{_d} : [magnet]({_url})" """

				_value = f"[{_hour}]\tDiffusion: <:green_circle:1047567792007819276>\nFlux: [AnimixPlay](https://animixplay.to/v1/{_page}/ep{int(_eps)})\t[SubsPlease](https://subsplease.org/shows/{_page}/)"

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

	@commands.command(aliases=["rtd", "lr"])
	async def ReleaseTheDoor(self, ctx):
		data = await self.s.latest_release()
		_guild = "0"
		if(hasattr(ctx.guild, "id")):
			_guild = ctx.guild.id

		_embed = self._process_latest_release(data, _guild, ctx)
		await ctx.send(embed=_embed)

	@commands.command(aliases=["dyd", "al"])
	async def DestroyYourDoor(self, ctx):
		data1 = await self.s.planning_anime()
		data2 = await self.s.latest_release()
		_guild = "0"
		if(hasattr(ctx.guild, "id")):
			_guild = ctx.guild.id
		
		embed1 = self._process_schedule_today(data1, _guild)
		embed2 = self._process_latest_release(data2, _guild, ctx)
		await ctx.send(embed=embed1)
		await ctx.send(embed=embed2)


		
def setup(bot):
	bot.add_cog(SubspleaseClient(bot))