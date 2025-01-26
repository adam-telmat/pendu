import random

class JeuPendu:
    def __init__(self):
        self.mot = ""
        self.lettres_trouvees = set()
        self.lettres_ratees = set()
        self.erreurs = 0
        self.max_erreurs = 7
        self.en_cours = True
        
    def charger_mot(self):
        with open("mots.txt", "r", encoding="utf-8") as fichier:
            mots = fichier.read().splitlines()
        self.mot = random.choice(mots).lower()
        
    def ajouter_mot(self, nouveau_mot):
        with open("mots.txt", "a", encoding="utf-8") as fichier:
            fichier.write(f"\n{nouveau_mot}")
            
    def afficher_mot_cache(self):
        return " ".join(lettre if lettre in self.lettres_trouvees else "_" for lettre in self.mot)
        
    def verifier_lettre(self, lettre):
        if not self.en_cours:
            return
            
        if lettre in self.mot:
            self.lettres_trouvees.add(lettre)
            if all(lettre in self.lettres_trouvees for lettre in self.mot):
                self.en_cours = False
        else:
            self.lettres_ratees.add(lettre)
            self.erreurs += 1
            if self.erreurs >= self.max_erreurs:
                self.en_cours = False

def menu_principal():
    while True:
        print("\nMenu principal :")
        print("1. Jouer")
        print("2. Ajouter un mot")
        print("3. Quitter")
        
        choix = input("Entrez votre choix (1, 2, 3) : ")
        
        if choix == "1":
            return "jouer"
        elif choix == "2":
            return "ajouter"
        elif choix == "3":
            return "quitter"

def ajouter_mot_interface():
    nouveau_mot = input("\nEntrez un nouveau mot à ajouter au jeu : ").lower()
    return nouveau_mot

def main():
    while True:
        choix = menu_principal()
        
        if choix == "jouer":
            jeu = JeuPendu()
            jeu.charger_mot()
            
            while True:
                print("\nMot à deviner : ", jeu.afficher_mot_cache())
                print("Lettres ratées : ", ", ".join(sorted(jeu.lettres_ratees)))
                print(f"Erreurs : {jeu.erreurs}/{jeu.max_erreurs}")
                
                if jeu.erreurs >= jeu.max_erreurs:
                    print(f"\nPerdu ! Le mot était : {jeu.mot}")
                    break
                elif all(lettre in jeu.lettres_trouvees for lettre in jeu.mot):
                    print("\nGagné !")
                    break
                
                lettre = input("\nEntrez une lettre : ").lower()
                if lettre.isalpha() and len(lettre) == 1:
                    jeu.verifier_lettre(lettre)
                else:
                    print("Veuillez entrer une lettre valide.")
                
        elif choix == "ajouter":
            nouveau_mot = ajouter_mot_interface()
            jeu = JeuPendu()
            jeu.ajouter_mot(nouveau_mot)
            print(f"Le mot '{nouveau_mot}' a été ajouté avec succès.")
            
        elif choix == "quitter":
            print("Au revoir!")
            break

if __name__ == "__main__":
    main()
