from reverse.client.reverse import Reverse
from reverse.core._models import Server, Message, Context
from discord.ext import commands
from discord.utils import get
import discord
from reverse.core import utils
import asyncio
import sys

class Bot(Reverse):
	
	def __new__(cls, command_prefix, description=None, **kwargs):
		return super(Bot, cls).__new__(cls)

	def __init__(self, command_prefix, description=None, **kwargs):
		super().__init__(command_prefix, description, **kwargs)
		sys.tracebacklimit = 1
		self.prefix = command_prefix
		self.description = description
		self.initKwargs = kwargs
		self.registerEvents()
		self.isShutingdown = False

	def registerEvents(self):
		self.getClient().event(self.on_ready)
		self.getClient().event(self.on_message)

	async def on_ready(self, ctx=None):
		print('We have logged in as {0.user} using Bot implementation'.format(self.getClient()))
	
	async def run(self, token: str, status: str = "starting"):
		await super().run(token=token)
		print("{} successfully".format(status))
	
	async def isShutingdown(self):
		return self.isShutingdown
				
		