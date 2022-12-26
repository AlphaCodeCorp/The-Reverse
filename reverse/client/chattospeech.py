from asyncio import sleep
from discord.ext import commands
from discord import Embed, FFmpegPCMAudio
import datetime
from reverse.core import utils
from reverse.core._service import SqliteService
from reverse.core._models import Message
import pyttsx3
import os




class ChatToSpeech(commands.Cog):

	"""This cog need PyNaCl and Pyttsx3 to work properly
	"""
	def __init__(self, bot):
		self.bot = bot
		self.room = []
		self.voicechannel = None
		self._basechannel = None
		self.engine = pyttsx3.init()
		self.voices = self.engine.getProperty('voices')
		self.engine.setProperty('voice', self.voices[0].id)
		self.engine.setProperty("rate", 175)
		self.queue = []
		self.tellnick = True

	@commands.command()
	async def rchangevoice(self, ctx, voiceid):
		"""Change text to speech voice, take an ID check rshowvoice

		Parameters
		----------
		ctx : Context
		"""
		_id = int(voiceid)
		if(_id < len(self.voices)):
			self.engine.setProperty("voice", self.voices[_id].id)
	
	@commands.command()
	async def rshowvoice(self, ctx):
		"""Show all voice available and their ID to use with rchangevoice

		Parameters
		----------
		ctx : _type_
			_description_
		"""
		_i = 0
		for e in self.voices:
			await ctx.send(f"{_i} - {e.name}")
			_i += 1
	
	@commands.command()
	async def rvoicespeed(self, ctx, rate):
		"""Change text to speech voice speedrate, 1 < 300

		Parameters
		----------
		ctx : Context
		rate : str
			speed number at which the bot will speak
		"""
		_rate = int(rate)
		if(_rate <= 300):
			self.engine.setProperty("rate", _rate)
	
	@commands.command()
	async def rvoicevolume(self, ctx, volume):
		"""Change text to speech voice volume, 0 < 1

		Parameters
		----------
		ctx : Context
			
		volume : str
			Volume at which the bot will speak
		"""
		from decimal import Decimal
		_volume = Decimal(volume)
		if(_volume <= 1):
			self.engine.setProperty("volume", _volume)
		
	@commands.command()
	async def rjoin(self, ctx):
		"""The bot will join the user voice channel

		Parameters
		----------
		ctx : Context
			
		"""
		author = ctx.message.author
		channel = author.voice.channel
		if(channel is None):
			await ctx.send("You are not connected to any voice channel.")
			pass
		self.voicechannel = await channel.connect()
		if(self.voicechannel):
			self._basechannel = channel
			self.room.append(ctx.channel.id)

	@commands.command()
	async def rquit(self, ctx):
		"""The bot will quit the voice channel he is in

		Parameters
		----------
		ctx : Context
		
		"""
		if(self.voicechannel):
			await self.voicechannel.disconnect()
			self.room = []

	@commands.command(aliases=["rsn"])
	async def rswapnick(self, ctx):
		"""Swap if the bot say your nickname or not

		Parameters
		----------
		ctx : Context
			
		"""
		self.tellnick = not self.tellnick

	@commands.Cog.listener()
	async def on_voice_state_update(self,data, *args):
		if(self._basechannel):
			if(len(self._basechannel.members) <= 1):
				try:
					await self.voicechannel.disconnect()
					self.voicechannel = None
				except:
					pass

	@commands.Cog.listener()
	async def on_message(self,message):
		_entryrooms = self.room
		_message = Message(message)
		if(message.channel.id in _entryrooms and not _message.getData().content.startswith("!")):
			print("Chat to Speech [{0.channel}] {0.content}".format(_message.getData()))
			engine = self.generate_engine()

			name = self.generate_file(engine, _message)

			self.queue.append(name)
			print(f"Chat added to queue {name}")
			if(self.voicechannel.is_playing() == False):
				self.voicechannel.play(FFmpegPCMAudio(name), after=self.start_playing)
			
	def generate_engine(self):
		engine = pyttsx3.init()
		return engine
	
	def generate_file(self, engine, message) -> str:
		name = "{0.id}.mp3".format(message.getData())

		if(self.tellnick):
			engine.save_to_file("{0.author.nick} a dit {0.content}".format(message.getData()), name)
		else:
			engine.save_to_file("{0.content}".format(message.getData()), name)
		engine.runAndWait()
		return name
	
	def start_playing(self, *args):
		if(len(self.queue) > 0 and self.voicechannel.is_playing() == False):
			try:
				os.remove(self.queue[0])
				self.queue.pop(0)
				self.voicechannel.play(FFmpegPCMAudio(self.queue[0]), after=self.start_playing)
			except:
				print("Queue Chat to Speech end.")
		

async def setup(bot):
	await bot.add_cog(ChatToSpeech(bot))
