import discord
from discord.ext import commands

# Remplacez 'your_token_here' par le token de votre bot
TOKEN = 'your_token_here'

# Définir les intents (permissions) que votre bot va utiliser
intents = discord.Intents.default()
intents.message_content = True

# Initialiser le bot avec un préfixe de commande
bot = commands.Bot(command_prefix='!', intents=intents)

# Événement lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Commande simple
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')
    
@bot.command()
async def triplecoucou(ctx):
    await ctx.send(f"Monstre {ctx.author.mention} dit coucou ! coucou ! coucou !")

# Lancer le bot
bot.run(TOKEN)
