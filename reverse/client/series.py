from discord.ext import commands
from discord import Embed
import datetime
from functools import wraps

from reverse.core._service.betaseries import *
from reverse.core._service import TaskService
from reverse.core._models import Context
from reverse.core import utils


class Worker(object):

	worker = []

	def register():
		"""A decorator that register method
		"""
		def wrapped(f, **kwargs):
			if(not f in Worker().worker):
				Worker().worker.append(f)
			return f
		return wrapped


class Series(commands.Cog):

	LOGO = "https://www.betaseries.com/images/site/betaseries.svg"
	
	def __init__(self, bot):
		self.bot = bot
		self.env = utils.load_backend().get("betaseries", {})
		self.token = self.env.get("api_key", None)
		self.user = self.env.get("user_key", None)

		self.b = BetaSeries(self.token, self.user)
		self.task = TaskService('Series')
		self.worker = Worker().worker
		
	@commands.command()
	async def recreate(self, token, user):
		"""Reset connection

		Parameters
		----------
		token : str
			API Token
		user : str
			User ID
		"""
		self.b = BetaSeries(token, user)

	@commands.command(aliases=['bstart'])
	async def betastart(self, ctx, *args):
		"""Create task that trigger worker at definied date

		Parameters
		----------
		ctx : :class:`reverse.core._models.Context`
			Context
		"""
		ctx = Context(ctx)
		_kwargs, _args = utils.parse_args(args)
		hour = _kwargs.get('hour', 7)
		DEFAULT_CALL = self.release_today

		# Coroutine next call Datetime
		next_call = utils.now() + datetime.timedelta(days=1)
		next_call = next_call.replace(hour=hour, minute=0, second=0)

		# Get delta from now until next_call
		delta = utils.time_until(next_call)
		data = {
			"Hour": 7,
			"Timer": delta,
			"Date": next_call
		}

		# Store method.__name__
		_task = _kwargs.get("task", DEFAULT_CALL.__name__)
		# Check if task is registered
		if(not any(e.__name__ == _task for e in self.worker)):
			await ctx.send("This worker is not compatible.")
			return
		
		try:
			# Test method
			callable(getattr(Series,_task))
			# Try to find if task already running
			if((_loop := self.task.findTaskByName(_task)) != None):
				_loop.stop()
				self.task.remove(_loop)
				await ctx.send("Overwrite betaseries task.")
			# Store method
			_task = getattr(self, _task)
			# Create loop with TaskService
			_loop = self.task.createLoop(_task, seconds=delta, ctx=ctx, data=data)
			# Start task
			self.task.start(_loop, load=_task, ctx=_loop.ctx, data=_loop.data)
			print("Betaseries task started. Delta : {} - Date : {}".format(delta, next_call))
		except Exception as e:
			print(e)

	@commands.command(aliases=['bstatus'])
	async def betastatus(self, ctx):
		ctx = Context(ctx)
		_loops = self.task.taskList()

		embed = Embed(title="Taches en cours", color=0xe80005, timestamp=datetime.datetime.today(), thumbnail=self.LOGO)
		if(len(_loops) > 0):
			for e in _loops:
				_value = ""
				_data = e.data
				for k,v in _data.items():
					_value += "> `{}`: {}\n".format(k,v)
				embed.add_field(name=e.getName(), value="Task is running : {}\n{}".format(e.isRunning(), _value), inline=False)
		else:
			embed.add_field(name="Aucune taches", value="Sadge", inline=False)
		embed.set_footer(text="".format("The Reverse"))

		await ctx.send(embed=embed)
	
	@commands.command(aliases=['brestart'])
	async def betarestart(self, ctx, *args):
		ctx = Context(ctx)
		_loops = self.task.taskList()
		_kwargs, _args = utils.parse_args(args)
		_found = _kwargs.get('task', "release_today")
		_kwargs.pop('task', None)

		for e in _loops:
			if(e.getName() == _found):
				if("stop" in args):
					if("force" in args):
						e.cancel()
						self.task.remove(e)
						await ctx.send("{} cold shutdown successfully.".format(_found))
						return
					e.stop()
					await ctx.send("{} warm shutdown. This will allows the task to finish its current iteration.".format(_found))
					return
				e.restart(**_kwargs)
				await ctx.send("{} restart successfully.".format(_found))

	@commands.command()
	async def pt(self, ctx):
		"""Alias for Planning Calendar today

		Parameters
		-----------
			ctx: :class:`reverse.core._models.Context`
		"""
		ctx = Context(ctx)
		await self.release_today(ctx=ctx)

	@commands.command()
	async def showWorker(self, ctx):
		await ctx.send("{}".format(self.worker))

	@Worker.register()
	async def release_today(self, **kwargs) -> None:
		"""Send embed listing today release from specified BetaSeries account

		Parameters
		-----------
			ctx: :class:`reverse.core._models.Context`
		"""
		ctx = kwargs['ctx']

		data = await self.planning_today()
		episodes = data.get('days', [])[0]

		embed=Embed(title="Sortie du jour", color=0xe80005, timestamp=datetime.datetime.today(), thumbnail=self.LOGO)
		if(len(episodes) > 0):
			for e in episodes['events']:
				e = e['payload']
				name = "{} {} — {}".format(e['show_title'], e['code'], e['title'])
				value = "[Source]({})".format(e['resource_url'])
				embed.add_field(name=name, value=value, inline=False)
		else:
			embed.add_field(name="Aucune sortie", value="N'oubliez pas d'ajouter de nouvelle séries sur Betaseries.", inline=False)
		embed.set_footer(text="".format("The Reverse"))

		await ctx.send(embed=embed)

	async def planning_member(self) -> dict:
		"""Return dictionnary of released planning of user
		"""
		r = Route('GET', '/planning/member')
		return await self.b.request(r)

	async def planning_today(self) -> dict:
		"""Return dictionnary of planning of today release from specified user
		"""
		today = datetime.date.today()
		r = Route('GET', '/planning/calendar', '&start={start}&end={end}&type={type}', start=today, end=today, type='all')
		return await self.b.request(r)


	
def setup(bot):
	bot.add_cog(Series(bot))