import requests

def choisir_mot():
    response = requests.get('https://trouve-mot.fr/api/random')
    if response.status_code == 200:
        mot_data = response.json()
        if isinstance(mot_data, list) and 'name' in mot_data[0]:
            return mot_data[0]['name']
        else:
            print("Erreur dans la structure de la réponse. Utilisation d'un mot par défaut.")
            return "default"
    else:
        print("Erreur lors de la récupération du mot. Utilisation d'un mot par défaut.")
        return "default"

def afficher_etat_courant(mot, lettres_devinees):
    affichage = [lettre if lettre in lettres_devinees else "_" for lettre in mot]
    return " ".join(affichage)

def pendu():
    mot = choisir_mot()
    lettres_devinees = set()
    essais = 6
    mot_trouve = False

    print("Bienvenue au jeu du pendu!")
    print(afficher_etat_courant(mot, lettres_devinees))
    print(f"Vous avez {essais} essais restants.")

    while essais > 0 and not mot_trouve:
        devinette = input("Devinez une lettre: ").lower()
        
        if len(devinette) != 1 or not devinette.isalpha():
            print("Veuillez entrer une seule lettre.")
            continue

        if devinette in lettres_devinees:
            print("Vous avez déjà deviné cette lettre.")
            continue

        lettres_devinees.add(devinette)

        if devinette in mot:
            print("Bonne réponse!")
        else:
            essais -= 1
            print("Mauvaise réponse.")
        
        etat_courant = afficher_etat_courant(mot, lettres_devinees)
        print(etat_courant)
        print(f"Vous avez {essais} essais restants.")

        if "_" not in etat_courant:
            mot_trouve = True

    if mot_trouve:
        print(f"Félicitations! Vous avez trouvé le mot: {mot}")
    else:
        print(f"Vous avez perdu. Le mot était: {mot}")

if __name__ == "__main__":
    pendu()
