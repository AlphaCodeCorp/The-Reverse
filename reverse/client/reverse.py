import asyncio
from discord.ext import commands
import discord
from reverse.core._models import Server, Message, Context
from reverse.core import utils, ReverseLogger
import random
from discord.utils import get

__title__ = 'The Reverse'
__author__ = 'Hveodrungr'
__copyright__ = 'Copyright 2015-2020 Rapptz'
__codename__ = 'T.H.O.M.A.S.'
__fullcodename__ = 'The Human Order Massively Aero Sexual'
__version__ = '0.2.1'
__logo__ = 'reverse\core\_store\logo\gurren-lagann.gif'

class Reverse():

	def __init__(self, command_prefix, description=None, **kwargs):
		print('Reverse : {}'.format(kwargs))
		intents = discord.Intents.all()
		self.client = Server(commands.Bot(command_prefix=command_prefix, description=description, kwargs=kwargs, intents=intents, status=discord.Status.offline))
		self.instance = self.getClient()
		self.cogs = []
		self.defaultCogs = ['reverse.client.core', 'reverse.client.default', 'reverse.client.debugger.debugger']
		self.toLoadCogs = utils.listCogs().keys()

		self.reverseNotepadLogger = ReverseLogger("ReverseNotepad", initLog=False)
		self.reverseNSALogger = ReverseLogger("ReverseNSA", consoleStream=True)
		self.reverseCountLogger = ReverseLogger("ReverseCount", initLog=False)

	async def run(self, token: str, cogs: list=[]):
		if(token is None):
			raise ValueError('Token can\t be empty.')
		if(not isinstance(token, str)):
			raise TypeError('Token is a string')
		self.token = token

		if(self.toLoadCogs):
			await self.linkCogs(self.toLoadCogs)
		else:
			await self.linkCogs(self.defaultCogs)
		
		self.running = await self.getClient().start(self.token)
		
	def getClient(self) -> commands.Bot:
		return self.client.getInstance()

	async def linkCogs(self, cogs: list):
		if(cogs is not None):
			self.cogs.extend(cogs)
		for cog in self.cogs:
			try:
				await self.getClient().load_extension(cog)
				print('Load {}'.format(cog))
			except Exception as e:
				print('{} cannot be loaded. [{}]'.format(cogs, e))
				self.getLogger()

	def getLogger(self):
		pass

	def getCommands(self) -> commands:
		return commands

	def createCommand(self, func, **kwargs) -> commands.Command:
		return commands.Command(func=func, kwargs=kwargs)

	def addCommand(self, _func, **kwargs) -> commands.command:
		command = commands.Command(func=_func, kwargs=kwargs)
		self.getClient().add_command(command)
		return command

	async def on_ready(self):
		print('We have logged in as {0.user}'.format(self.getClient()))
		
	async def on_message(self, message):
		m = Message(message)
		_attach = ""
		if(message.attachments):
			_attach+="\n"
			for i in utils.getObjectsAttr(message.attachments, "url"):
				_attach += "      -> {}\n".format(i)

		self.reverseNSALogger.info("[{0.channel}] <{0.guild}:{0.author}>: {0.content} {1}".format(m.getData(), _attach[:-1]))
		if(self.instance.user.mentioned_in(message)):
			self.reverseNotepadLogger.info("[{0.channel}] <{0.guild}:{0.author}>: {0.content} {1}".format(m.getData(), _attach[:-1]))

		ctx = Context(await self.getClient().get_context(message), __name__)

		await self.getClient().invoke(ctx)

	
	async def on_disconnect(self):
		print("Restart")
