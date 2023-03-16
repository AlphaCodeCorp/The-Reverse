import discord
from discord.ext import commands

ROLES = ["Mage", "Guerrier", "Voleur", "Paladin", "Nécromancien"]

class Roleplayer(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def rpjoin(self, ctx, role):
		# Ajouter un rôle au membre qui a envoyé la commande
		print(role)
		print(role in ROLES)
		if role in ROLES:
			guild = ctx.guild
			member = ctx.author
			role_obj = discord.utils.get(guild.roles, name=role)
			await member.add_roles(role_obj)
			await ctx.send(f"{member.mention} a rejoint la guilde des {role}s !")
		else:
			await ctx.send(f"{role} n'est pas un rôle valide.")

	@commands.command()
	async def rpleave(self, ctx, role):
		# Supprimer un rôle du membre qui a envoyé la commande
		print(role)
		print(role in ROLES)
		if role in ROLES:
			guild = ctx.guild
			member = ctx.author
			role_obj = discord.utils.get(guild.roles, name=role)
			await member.remove_roles(role_obj)
			await ctx.send(f"{member.mention} a quitté la guilde des {role}s.")
		else:
			await ctx.send(f"{role} n'est pas un rôle valide.")

async def setup(bot):
	await bot.add_cog(Roleplayer(bot))