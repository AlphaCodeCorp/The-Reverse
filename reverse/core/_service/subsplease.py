from urllib.parse import quote as _uriquote
import sys
import json
from .betaseries import json_or_text

import aiohttp

__version__ = "0.0.1"

class Route:
	BASE = "https://subsplease.org/api"
	PARAMETERS = ""

	def __init__(self, method, path, fields='', **parameters):
		self.path = path
		self.method = method
		url = (self.BASE + self.path + self.PARAMETERS + fields)
		if parameters:
			self.url = url.format(**{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
		else:
			self.url = url

class Subsplease:

	def __init__(self) -> None:
		self.name = "Subsplease"
		self._session = aiohttp.ClientSession()

		user_agent = "TheReverse (https://github.com/AlphaCodeCorp/The-Reverse {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
		self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

	def recreate(self) -> None:
		if(self._session.closed):
			self._session = aiohttp.ClientSession()
	
	async def request(self, route, *, files=None, **kwargs):
		method = route.method
		url = route.url

		headers = {
			'User-Agent': self.user_agent,
			'Content-Type': 'application/json'
		}

		async with self._session.request(method, url, **kwargs) as r:
			data = await json_or_text(r)

			if(300 > r.status >= 200):
				return data
			
			if(r.status == 400):
				self.errors(data)

	def errors(self, data):
		code = data["errors"][0].get("code", 0)
		text = data["errors"][0].get("text", "...")
		raise ValueError("{}: {}".format(code, text))

	async def planning_anime(self):
		r = Route('GET', '/?f=schedule&h=true&tz=Europe/Paris')
		s = await self.request(r)
		return s

	async def latest_release(self):
		r = Route('GET', '/?f=latest&tz=Europe/Paris')
		s = await self.request(r)
		return s
		