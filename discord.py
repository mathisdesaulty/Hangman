import discord
from discord.ext import commands

# Créer une instance du bot
bot = commands.Bot(command_prefix='!')

# Événement lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

# Commande ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Commande dire
@bot.command()
async def dire(ctx, *, message):
    await ctx.send(message)

# Lancer le bot
bot.run('TOKEN')