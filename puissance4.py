def initialiser_grille():
    return [[" " for _ in range(7)] for _ in range(6)]

def afficher_grille(grille):
    for ligne in grille:
        print("| " + " | ".join(ligne) + " |")
    print("+---" * 7 + "+")

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

def jouer():
    grille = initialiser_grille()
    afficher_grille(grille)
    joueurs = ["X", "O"]
    tour = 0

    while True:
        joueur = joueurs[tour % 2]
        try:
            colonne = int(input(f"Joueur {joueur}, choisissez une colonne (0-6) : "))
            if colonne < 0 or colonne > 6:
                print("Colonne invalide. Veuillez choisir une colonne entre 0 et 6.")
                continue
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entre 0 et 6.")
            continue

        if not placer_pion(grille, colonne, joueur):
            print("Cette colonne est pleine. Veuillez en choisir une autre.")
            continue

        afficher_grille(grille)

        if verifier_victoire(grille, joueur):
            print(f"Félicitations ! Le joueur {joueur} a gagné !")
            break

        if est_plein(grille):
            print("La grille est pleine. Match nul !")
            break

        tour += 1

if __name__ == "__main__":
    jouer()
1