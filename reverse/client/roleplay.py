import discord
from discord.ext import commands

from reverse.core._service import SqliteService
from reverse.core import utils

ROLES = ["Mage", "Guerrier", "Voleur", "Paladin", "Necromancien", "Chaman"]

class Roleplayer(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = SqliteService("Roleplay.db")
		self.c = self.db.instance.execute('''CREATE TABLE IF NOT EXISTS quests 
             (id INTEGER PRIMARY KEY, name TEXT, description TEXT, reward INTEGER)''')
		self.db.instance.commit()

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

	@commands.command()
	async def rpquests(self, ctx):
		# Afficher la liste des quêtes disponibles
		self.c.execute("SELECT id, name FROM quests")
		quests = self.c.fetchall()
		print(quests)
		if len(quests) > 0:
			message = "Voici la liste des quêtes disponibles :\n"
			for quest in quests:
				message += f"{quest[0]}. {quest[1]}\n"
			await ctx.send(message)
		else:
			await ctx.send("Il n'y a pas de quêtes disponibles pour le moment.")

	@commands.command()
	async def rpcreatequest(self, ctx, name, description, reward):
		""" _kwargs, _args = utils.parse_args(args) """
		# Créer une nouvelle quête
		if "MJ" in [role.name for role in ctx.author.roles]:
			print("MJ")
			self.c.execute("INSERT INTO quests (name, description, reward) VALUES (?, ?, ?)", (name, description, reward))
			self.db.instance.commit()

			await ctx.send(f"La quête iD:{self.c.lastrowid} \"{name}\" a été créée avec succès !\n {description}\n REWARD : {reward}")
		else:
			await ctx.send("Vous n'avez pas les permissions nécessaires pour créer une quête.")

	@commands.command()
	async def rpcomplete(self, ctx, quest_id):
		# Marquer une quête comme terminée
		self.c.execute("SELECT reward FROM quests WHERE id = ?", (quest_id,))
		reward = self.c.fetchone()
		print(reward)
		if reward:
			guild = ctx.guild
			member = ctx.author
			role_obj = discord.utils.get(guild.roles, name="Aventurier")
			await member.add_roles(role_obj)
			self.c.execute("DELETE FROM quests WHERE id = ?", (quest_id,))
			self.db.instance.commit()
			await ctx.send(f"{member.mention} a terminé la quête et a gagné {reward[0]} pièces d'or !")
		else:
			await ctx.send("Cette quête n'existe pas ou a déjà été terminée.")


async def setup(bot):
	await bot.add_cog(Roleplayer(bot))