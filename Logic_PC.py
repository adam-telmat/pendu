import random

def pendu():
    # Liste de mots possibles
    mots = ["python", "ordinateur", "programmation", "pendu", "jeu"]

    # Choisir un mot au hasard
    mot_a_deviner = random.choice(mots)
    lettres_devinees = []
    essais_restants = 6

    print("Bienvenue dans le jeu du pendu !")
    print("Le mot contient", len(mot_a_deviner), "lettres.")

    while essais_restants > 0:
        # Affichage du mot avec les lettres devinées
        mot_affiche = ""
        for lettre in mot_a_deviner:
            if lettre in lettres_devinees:
                mot_affiche += lettre
            else:
                mot_affiche += "_"
        
        print("\nMot :", mot_affiche)

        # Vérifier si le joueur a gagné
        if "_" not in mot_affiche:
            print("\nFélicitations ! Vous avez trouvé le mot :", mot_a_deviner)
            break

        # Demander une lettre
        lettre = input("Proposez une lettre : ").lower()

        if lettre in lettres_devinees:
            print("Vous avez déjà proposé cette lettre.")
        elif lettre in mot_a_deviner:
            print("Bonne lettre !")
            lettres_devinees.append(lettre)
        else:
            print("Lettre incorrecte.")
            essais_restants -= 1
            lettres_devinees.append(lettre)
            print("Il vous reste", essais_restants, "essais.")

    if essais_restants == 0:
        print("\nDommage ! Le mot était :", mot_a_deviner)

# Lancer le jeu
pendu()