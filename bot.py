import discord
import requests
from discord.ext import commands

TOKEN = 'token'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)



games = {}

def choose_word():
    response = requests.get('https://trouve-mot.fr/api/random')
    if response.status_code == 200:
        word_data = response.json()
        if isinstance(word_data, list) and 'name' in word_data[0]:
            return word_data[0]['name']
        else:
            print("Erreur dans la structure de la réponse. Utilisation d'un mot par défaut.")
            return "default"
    else:
        print("Erreur lors de la récupération du mot. Utilisation d'un mot par défaut.")
        return "default"

def display_current_state(word, guessed_letters):
    display = [letter if letter in guessed_letters else "~" for letter in word]
    return " ".join(display)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')
    
@bot.command()
async def triplecoucou(ctx):
    await ctx.send(f"Monstre {ctx.author.mention} dit coucou ! coucou ! coucou !")


@bot.command()
async def start(ctx):
    word = choose_word()
    games[ctx.author.id] = {
        "word": word,
        "guessed_letters": set(),
        "tries": 6,
        "guessed_word": False
    }
    await ctx.send("Bienvenue au jeu du pendu!")
    await ctx.send(display_current_state(word, set()))
    await ctx.send(f"Vous avez 6 essais restants.")

@bot.command()
async def guess(ctx, letter: str):
    if ctx.author.id not in games:
        await ctx.send("Vous devez commencer un nouveau jeu avec !start")   
        return

    game = games[ctx.author.id]
    word = game["word"]
    guessed_letters = game["guessed_letters"]
    tries = game["tries"]
    guessed_word = game["guessed_word"]

    if len(letter) != 1 or not letter.isalpha():
        await ctx.send("Veuillez entrer une seule lettre.")
        return

    letter = letter.lower()

    if letter in guessed_letters:
        await ctx.send("Vous avez déjà deviné cette lettre.")
        return

    guessed_letters.add(letter)

    if letter in word:
        await ctx.send("Bonne réponse!")
    else:
        game["tries"] -= 1
        await ctx.send("Mauvaise réponse.")

    current_state = display_current_state(word, guessed_letters)
    await ctx.send(current_state)
    await ctx.send(f"Vous avez {game['tries']} essais restants.")

    if "~" not in current_state:
        game["guessed_word"] = True
        await ctx.send(f"Félicitations! Vous avez trouvé le mot: {word}")
        del games[ctx.author.id]
    elif game["tries"] <= 0:
        await ctx.send(f"Vous avez perdu. Le mot était: {word}")
        del games[ctx.author.id]

@bot.command()
async def guessWord(ctx, word: str):
    if ctx.author.id not in games:
        await ctx.send("Vous devez commencer un nouveau jeu avec !start")   
        return
    game = games[ctx.author.id]
    if word == game["word"]:
        game["guessed_word"] = True
        await ctx.send(f"Félicitations! Vous avez trouvé le mot: {word}")
        del games[ctx.author.id]
    else:
        game["tries"] -= 1
        await ctx.send("Mauvaise réponse.")
        current_state = display_current_state(word, "_")
        await ctx.send(current_state)
        await ctx.send(f"Vous avez {game['tries']} essais restants.")
        if game["tries"] <= 0:
            await ctx.send(f"Vous avez perdu. Le mot était: {game['word']}")
            del games[ctx.author.id]


# Lancer le bot
bot.run(TOKEN)
