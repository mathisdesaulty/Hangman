import requests

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
    display = [letter if letter in guessed_letters else "_" for letter in word]
    return " ".join(display)

def hangman():
    word = choose_word()
    guessed_letters = set()
    tries = 6
    guessed_word = False

    print("Bienvenue au jeu du pendu!")
    print(display_current_state(word, guessed_letters))
    print(f"Vous avez {tries} essais restants.")

    while tries > 0 and not guessed_word:
        guess = input("Devinez une lettre: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Veuillez entrer une seule lettre.")
            continue

        if guess in guessed_letters:
            print("Vous avez déjà deviné cette lettre.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print("Bonne réponse!")
        else:
            tries -= 1
            print("Mauvaise réponse.")
        
        current_state = display_current_state(word, guessed_letters)
        print(current_state)
        print(f"Vous avez {tries} essais restants.")

        if "_" not in current_state:
            guessed_word = True

    if guessed_word:
        print(f"Félicitations! Vous avez trouvé le mot: {word}")
    else:
        print(f"Vous avez perdu. Le mot était: {word}")

if __name__ == "__main__":
    hangman()
