import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)

# Configuration de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Pendu")

# Configuration du texte
police = pygame.font.Font(None, 36)

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

    def dessiner_pendu(self):
        # Base - La ligne horizontale du bas
        pygame.draw.line(fenetre, NOIR, (100, 500), (300, 500), 8)
        
        if self.erreurs > 0:
            # Poteau vertical
            pygame.draw.line(fenetre, NOIR, (200, 500), (200, 100), 8)
        
        if self.erreurs > 1:
            # Poteau horizontal du haut
            pygame.draw.line(fenetre, NOIR, (200, 100), (400, 100), 8)
        
        if self.erreurs > 2:
            # Corde
            pygame.draw.line(fenetre, NOIR, (400, 100), (400, 150), 8)
        
        if self.erreurs > 3:
            # Tête (un cercle)
            pygame.draw.circle(fenetre, NOIR, (400, 175), 25, 8)
        
        if self.erreurs > 4:
            # Corps
            pygame.draw.line(fenetre, NOIR, (400, 200), (400, 300), 8)
        
        if self.erreurs > 5:
            # Bras (deux lignes)
            pygame.draw.line(fenetre, NOIR, (400, 225), (350, 275), 8)
            pygame.draw.line(fenetre, NOIR, (400, 225), (450, 275), 8)
        
        if self.erreurs > 6:
            # Jambes (deux lignes)
            pygame.draw.line(fenetre, NOIR, (400, 300), (350, 375), 8)
            pygame.draw.line(fenetre, NOIR, (400, 300), (450, 375), 8)

def menu_principal():
    while True:
        fenetre.fill(BLANC)
        
        texte_jouer = police.render("1. Jouer", True, NOIR)
        texte_ajouter = police.render("2. Ajouter un mot", True, NOIR)
        texte_quitter = police.render("3. Quitter", True, NOIR)
        
        fenetre.blit(texte_jouer, (LARGEUR//2 - 100, HAUTEUR//2 - 50))
        fenetre.blit(texte_ajouter, (LARGEUR//2 - 100, HAUTEUR//2))
        fenetre.blit(texte_quitter, (LARGEUR//2 - 100, HAUTEUR//2 + 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "jouer"
                elif event.key == pygame.K_2:
                    return "ajouter"
                elif event.key == pygame.K_3:
                    return "quitter"

def ajouter_mot_interface():
    nouveau_mot = ""
    en_saisie = True
    
    while en_saisie:
        fenetre.fill(BLANC)
        texte_instruction = police.render("Entrez un nouveau mot (Entrée pour valider):", True, NOIR)
        texte_mot = police.render(nouveau_mot, True, BLEU)
        
        fenetre.blit(texte_instruction, (50, HAUTEUR//2 - 50))
        fenetre.blit(texte_mot, (50, HAUTEUR//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nouveau_mot:
                    return nouveau_mot
                elif event.key == pygame.K_BACKSPACE:
                    nouveau_mot = nouveau_mot[:-1]
                elif event.unicode.isalpha():
                    nouveau_mot += event.unicode.lower()

def main():
    while True:
        choix = menu_principal()
        
        if choix == "jouer":
            jeu = JeuPendu()
            jeu.charger_mot()
            
            while True:
                fenetre.fill(BLANC)
                jeu.dessiner_pendu()
                
                # Affichage du mot caché
                texte_mot = police.render(jeu.afficher_mot_cache(), True, NOIR)
                fenetre.blit(texte_mot, (LARGEUR//2 - 100, 400))
                
                # Affichage des lettres ratées
                if jeu.lettres_ratees:
                    texte_ratees = police.render(f"Lettres ratées : {', '.join(sorted(jeu.lettres_ratees))}", True, (255, 0, 0))
                    fenetre.blit(texte_ratees, (50, 50))
                
                # Affichage du nombre d'erreurs
                texte_erreurs = police.render(f"Erreurs : {jeu.erreurs}/{jeu.max_erreurs}", True, NOIR)
                fenetre.blit(texte_erreurs, (LARGEUR - 200, 50))
                
                # Affichage du message de fin
                if not jeu.en_cours:
                    if jeu.erreurs >= jeu.max_erreurs:
                        message = f"Perdu ! Le mot était : {jeu.mot}"
                    else:
                        message = "Gagné !"
                    texte_fin = police.render(message, True, BLEU)
                    fenetre.blit(texte_fin, (LARGEUR//2 - 150, 450))
                    texte_retour = police.render("Appuyez sur ESPACE pour revenir au menu", True, NOIR)
                    fenetre.blit(texte_retour, (LARGEUR//2 - 250, 500))
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if not jeu.en_cours and event.key == pygame.K_SPACE:
                            break
                        if event.unicode.isalpha():
                            jeu.verifier_lettre(event.unicode.lower())
                
                if not jeu.en_cours and pygame.key.get_pressed()[pygame.K_SPACE]:
                    break
                    
        elif choix == "ajouter":
            nouveau_mot = ajouter_mot_interface()
            jeu = JeuPendu()
            jeu.ajouter_mot(nouveau_mot)
            
        elif choix == "quitter":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main() 