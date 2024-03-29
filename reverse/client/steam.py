from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import discord
from discord.ext import commands
from discord import Embed
import datetime
from reverse.core._service import SqliteService
from reverse.core import utils


class SteamScraper(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		options = webdriver.Chrome()
		options.headless = True
		self.driver = webdriver.Chrome(options=options)

	@commands.command(aliases=['tsteam'])
	async def trendingsteam(self, ctx):
		"""Return Trending top 10 steam game

		Parameters
		----------
		ctx : Context
			
		"""
		embed = self.get_all("https://store.steampowered.com/search/?filter=trending")

		await ctx.send(embed=embed)
	
	@commands.command(aliases=['testeam'])
	async def trendingevaluationsteam(self, ctx):
		"""Return Trending top 10 by evaluation

		Parameters
		----------
		ctx : Context
		
		"""
		embed = self.get_all("https://store.steampowered.com/search/?sort_by=Reviews_DESC&filter=trending&ndl=1", name="Trending Steam by User Evaluation")

		await ctx.send(embed=embed)

	@commands.command(aliases=['lrsteam'])
	async def lastreleasesteam(self, ctx):
		"""Return steam last released game

		Parameters
		----------
		ctx : Context
			
		"""
		embed = self.get_all("https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&ndl=1", name="Last release")

		await ctx.send(embed=embed)

	@commands.command(aliases=['prsteam'])
	async def popularreleasesteam(self, ctx):
		"""Return popular last released game

		Parameters
		----------
		ctx : Context
			
		"""
		embed = self.get_all("https://store.steampowered.com/search/?filter=popularnew&sort_by=Released_DESC&os=win", name="Popular release")

		await ctx.send(embed=embed)

	def get_all(self, url, name="Trending Steam") -> Embed:
		"""Scrap steam search page and create an embed of the first 10 items

		Parameters
		----------
		url : string
			steam search page
		name : str, optional
			Title of the embed, by default "Trending Steam"

		Returns
		-------
		Embed
		"""
		self.driver.get(url)

		url = self.driver.find_elements("xpath", "//a[@class='search_result_row ds_collapse_flag ']")
		titles = self.driver.find_elements("xpath", "//span[@class='title']")
		releases = self.driver.find_elements("xpath", "//div[@class='col search_released responsive_secondrow']")
		prices = self.driver.find_elements("xpath", "//div[@class='col search_price  responsive_secondrow' or @class='col search_price discounted responsive_secondrow']")
		i = 0

		embed = Embed(title=name, color=0x2f7fc2, timestamp=datetime.datetime.today())
		for title in titles:
			price = prices[i].text.split('\n')
			release = releases[i].text
			if(len(price) > 1):
				price[0] = utils.strike(price[0])
			if(not release):
				release = "Unknown"
			if(len(price) > 1):
				embed.add_field(name=title.text, value=f"[link]({url[i].get_attribute('href')}) Release date : {release}, Price: {price[0]} Discount: {price[1]}", inline=False)
				print(f"{i} - {title.text} - {release} - {price[0]} soldes {price[1]}")
			else:
				embed.add_field(name=title.text, value=f"[link]({url[i].get_attribute('href')}) Release date : {release}, Price: {price[0]}", inline=False)
				print(f"{i} - {title.text} - {release} - {price[0]}")
			if((i := i + 1) > 10):
				break
		embed.set_footer(text="".format("The Reverse"))

		self.driver.quit()
		return embed

async def setup(bot):
	await bot.add_cog(SteamScraper(bot))