import pygame
import random
import os

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Chemin du fichier des mots
MOTS_FICHIER = "mots.txt"


class Pendu:
    """Classe pour gérer l'affichage du pendu."""
    def __init__(self):
        self.stages = [
            """
               -----
               |   |
               |
               |
               |
               |
            ---------
            """,
            """
               -----
               |   |
               |   O
               |
               |
               |
            ---------
            """,
            """
               -----
               |   |
               |   O
               |   |
               |
               |
            ---------
            """,
            """
               -----
               |   |
               |   O
               |  /|
               |
               |
            ---------
            """,
            """
               -----
               |   |
               |   O
               |  /|\\
               |
               |
            ---------
            """,
            """
               -----
               |   |
               |   O
               |  /|\\
               |  /
               |
            ---------
            """,
            """
               -----
               |   |
               |   O
               |  /|\\
               |  / \\
               |
            ---------
            """
        ]

    def afficher(self, screen, erreurs):
        """Affiche le pendu en fonction du nombre d'erreurs."""
        font = pygame.font.SysFont("courier", 24)
        lines = self.stages[erreurs].strip().split("\n")
        x, y = 50, 50
        for line in lines:
            rendered_line = font.render(line, True, BLACK)
            screen.blit(rendered_line, (x, y))
            y += 25


class JeuPendu:
    """Classe principale pour gérer le jeu du pendu."""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jeu du Pendu")
        self.font = pygame.font.SysFont("arial", 32)
        self.pendu = Pendu()

    def charger_mots(self):
        """Charge les mots depuis un fichier."""
        if not os.path.exists(MOTS_FICHIER):
            with open(MOTS_FICHIER, "w") as f:
                pass
        with open(MOTS_FICHIER, "r") as f:
            return [ligne.strip() for ligne in f.readlines() if ligne.strip()]

    def ajouter_mot(self, mot):
        """Ajoute un mot dans le fichier."""
        with open(MOTS_FICHIER, "a") as f:
            f.write(mot + "\n")

    def ajouter_mot_interface(self):
        """Interface pour ajouter un mot."""
        input_active = True
        mot = ""
        while input_active:
            self.screen.fill(WHITE)
            titre = self.font.render("Ajoutez un mot :", True, BLACK)
            texte = self.font.render(mot, True, RED)
            self.screen.blit(titre, (50, 100))
            self.screen.blit(texte, (50, 200))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if mot:
                            self.ajouter_mot(mot)
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        mot = mot[:-1]
                    else:
                        mot += event.unicode

    def afficher_bouton(self, texte, x, y, w, h, couleur, survol_couleur):
        """Affiche un bouton interactif."""
        souris = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        if x + w > souris[0] > x and y + h > souris[1] > y:
            pygame.draw.rect(self.screen, survol_couleur, (x, y, w, h))
            if clique[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, couleur, (x, y, w, h))

        texte_render = self.font.render(texte, True, BLACK)
        self.screen.blit(texte_render, (x + (w - texte_render.get_width()) // 2, y + (h - texte_render.get_height()) // 2))
        return False

    def menu_principal(self):
        """Affiche le menu principal."""
        running = True
        while running:
            self.screen.fill(WHITE)
            titre = self.font.render("Jeu du Pendu", True, BLACK)
            self.screen.blit(titre, (SCREEN_WIDTH // 2 - titre.get_width() // 2, 100))

            jouer = self.afficher_bouton("Jouer", 300, 200, 200, 50, GRAY, BLUE)
            ajouter = self.afficher_bouton("Ajouter un mot", 300, 300, 200, 50, GRAY, BLUE)
            quitter = self.afficher_bouton("Quitter", 300, 400, 200, 50, GRAY, BLUE)

            pygame.display.flip()

            if jouer:
                self.jouer_partie()
            elif ajouter:
                self.ajouter_mot_interface()
            elif quitter:
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def jouer_partie(self):
        """Lance une partie du jeu."""
        mots = self.charger_mots()
        if not mots:
            self.afficher_message("Pas de mots disponibles !")
            return

        mot = random.choice(mots).lower()
        lettres_trouvees = set()
        lettres_ratees = set()
        tentatives = 6

        running = True
        while running:
            self.screen.fill(WHITE)

            # Affichage du mot à deviner
            mot_affiche = " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])
            mot_render = self.font.render(mot_affiche, True, BLACK)
            self.screen.blit(mot_render, (50, 100))

            # Lettres ratées
            lettres_ratees_render = self.font.render("Lettres ratées : " + ", ".join(lettres_ratees), True, RED)
            self.screen.blit(lettres_ratees_render, (50, 200))

            # Tentatives restantes
            tentatives_render = self.font.render(f"Tentatives restantes : {tentatives}", True, BLACK)
            self.screen.blit(tentatives_render, (50, 250))

            # Afficher le pendu
            self.pendu.afficher(self.screen, 6 - tentatives)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    lettre = event.unicode.lower()
                    if lettre.isalpha() and len(lettre) == 1:
                        if lettre in mot and lettre not in lettres_trouvees:
                            lettres_trouvees.add(lettre)
                        elif lettre not in lettres_ratees:
                            lettres_ratees.add(lettre)
                            tentatives -= 1

            # Vérification des conditions de victoire/défaite
            if tentatives == 0:
                self.afficher_message(f"Perdu ! Le mot était : {mot}")
                running = False
            elif all(lettre in lettres_trouvees for lettre in mot):
                self.afficher_message("Gagné !")
                running = False

    def afficher_message(self, message):
        """Affiche un message temporaire."""
        self.screen.fill(WHITE)
        texte = self.font.render(message, True, BLACK)
        self.screen.blit(texte, (SCREEN_WIDTH // 2 - texte.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    def run(self):
        """Lance le jeu."""
        self.menu_principal()
        pygame.quit()


if __name__ == "__main__":
    jeu = JeuPendu()
    jeu.run()