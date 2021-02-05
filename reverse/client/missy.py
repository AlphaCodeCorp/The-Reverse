from discord.ext import commands
from discord import Guild
import asyncio
from urllib import parse
from reverse.core._service import SqliteService
from reverse.core._models import Context, Role
from reverse.core import utils

class Missy(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = SqliteService()
		self.schedule = []

	@commands.command()
	async def whoismissy(self, ctx):
		await ctx.send("Une horreur lovecraftienne... Tempus edax rerum.")
	
	async def debugSQL(self, ctx, table="missy", column="id integer PRIMARY KEY, name text"):
		self.db.createTable(table, column)

	@commands.command()
	async def showTable(self, ctx):
		record = self.db._fetchAll(self.db.listTable())
		for v in record:
			await ctx.send("Table {}.".format(*v))

	async def tableToList(self, ctx) -> list:
		await ctx.send(SqliteService.tableToList(self.db.listTable()))

	@commands.command()
	async def debugInsertAllMembers(self, ctx):
		guild = ctx.guild
		await ctx.send("Fetch all members from {} called by {}".format(ctx.guild.name, ctx.author.name))
		self.db.createTable(guild.name, "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, discordID TEXT, UNIQUE(id, discordID)")
		for v in guild.members:
			self.db.insertion(guild.name, ["name", "discordID"], [v.name, str(v.id)], ignore=True)
		await ctx.send("Successfully inserted {} entries to Table {} ".format(len(guild.members), guild.name))

	@commands.command()
	async def initServerEvent(self, ctx):
		ctx = Context(ctx)
		guild = ctx.guild
		table = "{}_event".format(guild.name)
		if(self.db.isTableExist(table)):
			await ctx.send("Starting initialization to host event on this server.")
			self.db.createTable("{}_event".format(guild.name), "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, role TEXT")
			return
		await ctx.send("Server already initalized.")

	@commands.command()
	async def members(self, ctx, *args):
		ctx = Context(ctx)
		guild = ctx.guild
		_kwargs, _args = utils.parse_args(args)
		if("role" in _kwargs.keys()):
			r_id = _kwargs["role"][3:-1]
			_m = utils.getAllMembers(guild, int(r_id))

			if(len(_m) >= 1):
				for v in _m:
					await ctx.send("User: {}".format(v))
			else:
				await ctx.send("This role is unused.")

	def getLearners(self, ctx):

		apprenants = []
		roles = []

		for r in ctx.guild.roles:
			roles.append([r.id, r.name])

		await ctx.send(roles)

		await ctx.send("------------------------------")

		for m in ctx.guild.members:
			apprenants.append([m.name, m.id, m.roles])

		await ctx.send(apprenants)

def setup(bot):
	bot.add_cog(Missy(bot))