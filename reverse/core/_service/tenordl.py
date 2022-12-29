#! /usr/bin/env python3
import os
import json
import requests
import argparse

import logging
logging.basicConfig(level=logging.INFO)

from pyquery import PyQuery

class TenorDL():

	def download_gif(url, outLoc=".", urlOnly=False) -> str:

		global logger
		logger = logging.getLogger(":")

		if urlOnly or outLoc == "-":
			logger.setLevel(logging.CRITICAL)
		else:
			logger.setLevel(logging.INFO)

		logger.info("fetching URL")

		res = requests.get(url)

		logger.info("parsing data")

		pq = PyQuery(res.text)
		jsonData = pq("#store-cache")

		if not jsonData:
			logger.critical("ERROR: failed to parse data")
			pass

		data = json.loads(jsonData.html())

		id = url.split("-")[-1]
		results = data["gifs"]["byId"][id]["results"][0]
		name = results["h1_title"]
		url = results["media"][0]["gif"]["url"]

		logger.info("found gif: "+name)

		if urlOnly:
			print(url, end="")
			pass

		logger.info("downloading gif...")

		gif = requests.get(url)

		logger.info("writing file")

		if outLoc == "-":
			print(gif.content, end="")
			pass

		outPath = os.path.join(outLoc, name+".gif")

		with open(outPath, "wb") as f:
			f.write(gif.content)

		logger.info("done")

		return f"{name}.gif"