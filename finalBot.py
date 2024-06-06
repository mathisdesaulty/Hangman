import discord
import requests
from discord.ext import commands

TOKEN = 'token'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)



hang = {}

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


tictactoe = {}

def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def display_board(board):
    return "\n".join([" | ".join(row) for row in board])

def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_full(board):
    return all([cell != " " for row in board for cell in row])


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
async def startHangman(ctx):
    word = choose_word()
    hang[ctx.author.id] = {
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
    if ctx.author.id not in hang:
        await ctx.send("Vous devez commencer un nouveau jeu avec !start")   
        return

    game = hang[ctx.author.id]
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
        del hang[ctx.author.id]
    elif game["tries"] <= 0:
        await ctx.send(f"Vous avez perdu. Le mot était: {word}")
        del hang[ctx.author.id]

@bot.command()
async def guessWord(ctx, word: str):
    if ctx.author.id not in hang:
        await ctx.send("Vous devez commencer un nouveau jeu avec !start")   
        return
    game = hang[ctx.author.id]
    if word == game["word"]:
        game["guessed_word"] = True
        await ctx.send(f"Félicitations! Vous avez trouvé le mot: {word}")
        del hang[ctx.author.id]
    else:
        game["tries"] -= 1
        await ctx.send("Mauvaise réponse.")
        current_state = display_current_state(word, "_")
        await ctx.send(current_state)
        await ctx.send(f"Vous avez {game['tries']} essais restants.")
        if game["tries"] <= 0:
            await ctx.send(f"Vous avez perdu. Le mot était: {game['word']}")
            del hang[ctx.author.id]

@bot.command()
async def startTicTacToe(ctx, opponent: discord.Member):
    if ctx.author.id in tictactoe or opponent.id in tictactoe:
        await ctx.send("Un des joueurs est déjà dans une partie.")
        return

    tictactoe[ctx.author.id] = {
        "board": initialize_board(),
        "turn": ctx.author.id,
        "players": [ctx.author.id, opponent.id]
    }
    tictactoe[opponent.id] = tictactoe[ctx.author.id]

    await ctx.send(f"{ctx.author.mention} a commencé un jeu de morpion avec {opponent.mention}!")
    await ctx.send(display_board(tictactoe[ctx.author.id]["board"]))
    await ctx.send(f"C'est au tour de {ctx.author.mention} (X)")

@bot.command()
async def play(ctx, row: int, col: int):
    if ctx.author.id not in tictactoe:
        await ctx.send("Vous devez commencer un nouveau jeu avec !start")
        return

    game = tictactoe[ctx.author.id]
    if game["turn"] != ctx.author.id:
        await ctx.send("Ce n'est pas votre tour.")
        return

    board = game["board"]
    player_symbol = "X" if game["turn"] == game["players"][0] else "O"

    if row < 1 or row > 3 or col < 1 or col > 3:
        await ctx.send("Les indices de ligne et de colonne doivent être entre 1 et 3.")
        return

    if board[row - 1][col - 1] != " ":
        await ctx.send("Cette case est déjà occupée. Choisissez-en une autre.")
        return

    board[row - 1][col - 1] = player_symbol

    if check_winner(board, player_symbol):
        await ctx.send(display_board(board))
        await ctx.send(f"Félicitations {ctx.author.mention}, vous avez gagné !")
        del tictactoe[game["players"][0]]
        del tictactoe[game["players"][1]]
        return

    if is_full(board):
        await ctx.send(display_board(board))
        await ctx.send("C'est un match nul !")
        del tictactoe[game["players"][0]]
        del tictactoe[game["players"][1]]
        return

    game["turn"] = game["players"][0] if game["turn"] == game["players"][1] else game["players"][1]
    next_player = bot.get_user(game["turn"])
    await ctx.send(display_board(board))
    await ctx.send(f"C'est au tour de {next_player.mention} ({'X' if game['turn'] == game['players'][0] else 'O'})")
    
@bot.command()
async def stop(ctx):
    game = tictactoe[ctx.author.id]
    if ctx.author.id not in tictactoe:
        await ctx.send("Vous devez commencer un nouveau jeu avec !start")
        return
    del tictactoe[game["players"][0]]
    del tictactoe[game["players"][1]]
    await ctx.send("La partie a été arrêtée.")
    
@bot.command()
async def commandes(ctx):
    await ctx.send("Bienvenue dans l'aide de ce bot !\n\n"
                   "Voici la liste des commandes disponibles :\n"
                   "!hello : Affiche un message de bienvenue\n"
                   "!triplecoucou : Monstre dit coucou 3 fois\n"
                   "!startHangman : Commence une partie de pendu\n"
                   "!guess <lettre> : Propose une lettre pour le pendu\n"
                   "!guessWord <mot> : Propose un mot pour le pendu\n"
                   "!startTicTacToe <@joueur> : Commence une partie de morpion avec un joueur\n"
                   "!play <ligne> <colonne> : Joue un coup dans la partie de morpion\n"
                   "!stop : Arrête la partie de morpion en cours\n"
                   "!help : Affiche l'aide du bot")

games = {}

def initialiser_grille():
    return [[" " for _ in range(7)] for _ in range(6)]

def afficher_grille(grille):
    lignes = ["| " + " | ".join(ligne) + " |" for ligne in grille]
    return "\n".join(lignes) + "\n" + "+---" * 7 + "+"

def placer_pion(grille, colonne, pion):
    for ligne in reversed(grille):
        if ligne[colonne] == " ":
            ligne[colonne] = pion
            return True
    return False

def verifier_victoire(grille, pion):
    # Vérifier les lignes
    for ligne in grille:
        for i in range(4):
            if ligne[i] == ligne[i+1] == ligne[i+2] == ligne[i+3] == pion:
                return True
    
    # Vérifier les colonnes
    for col in range(7):
        for ligne in range(3):
            if grille[ligne][col] == grille[ligne+1][col] == grille[ligne+2][col] == grille[ligne+3][col] == pion:
                return True

    # Vérifier les diagonales (haut-gauche à bas-droite)
    for ligne in range(3):
        for col in range(4):
            if grille[ligne][col] == grille[ligne+1][col+1] == grille[ligne+2][col+2] == grille[ligne+3][col+3] == pion:
                return True

    # Vérifier les diagonales (bas-gauche à haut-droite)
    for ligne in range(3, 6):
        for col in range(4):
            if grille[ligne][col] == grille[ligne-1][col+1] == grille[ligne-2][col+2] == grille[ligne-3][col+3] == pion:
                return True

    return False

def est_plein(grille):
    return all(grille[0][col] != " " for col in range(7))


@bot.command()
async def start4(ctx, adversaire: discord.Member):
    if ctx.author.id in games or adversaire.id in games:
        await ctx.send("Un des joueurs a déjà une partie en cours. Terminez-la avant de commencer une nouvelle.")
        return
    
    games[ctx.author.id] = {
        "grille": initialiser_grille(),
        "joueurs": [ctx.author.id, adversaire.id],
        "tour": 0
    }
    games[adversaire.id] = games[ctx.author.id]

    await ctx.send(f"Jeu de Puissance 4 commencé entre {ctx.author.mention} (X) et {adversaire.mention} (O) !")
    await ctx.send("```\n" + afficher_grille(games[ctx.author.id]["grille"]) + "\n```")
    await ctx.send(f"C'est au tour de {ctx.author.mention} (X)")

@bot.command()
async def play4(ctx, colonne: int):
    if ctx.author.id not in games:
        await ctx.send("Vous devez commencer un nouveau jeu avec !start")
        return

    game = games[ctx.author.id]
    grille = game["grille"]
    joueur = game["joueurs"][game["tour"] % 2]

    if ctx.author.id != joueur:
        await ctx.send("Ce n'est pas votre tour.")
        return

    pion = "X" if joueur == game["joueurs"][0] else "O"

    if colonne < 0 or colonne > 6:
        await ctx.send("Colonne invalide. Veuillez choisir une colonne entre 0 et 6.")
        return

    if not placer_pion(grille, colonne, pion):
        await ctx.send("Cette colonne est pleine. Veuillez en choisir une autre.")
        return

    await ctx.send("```\n" + afficher_grille(grille) + "\n```")

    if verifier_victoire(grille, pion):
        await ctx.send(f"Félicitations ! Le joueur {pion} ({ctx.author.mention}) a gagné !")
        del games[game["joueurs"][0]]
        del games[game["joueurs"][1]]
        return

    if est_plein(grille):
        await ctx.send("La grille est pleine. Match nul !")
        del games[game["joueurs"][0]]
        del games[game["joueurs"][1]]
        return

    game["tour"] += 1
    joueur_suivant = bot.get_user(game["joueurs"][game["tour"] % 2])
    pion_suivant = "X" if game["tour"] % 2 == 0 else "O"
    await ctx.send(f"C'est au tour de {joueur_suivant.mention} ({pion_suivant})")
# Lancer le bot
bot.run(TOKEN)