import pygame

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

# Fonction pour dessiner le pendu
def dessiner_pendu(tentatives):
    if tentatives == 5:
        pygame.draw.circle(fenetre, NOIR, (400, 150), 30)  # Tête
    if tentatives == 4:
        pygame.draw.line(fenetre, NOIR, (400, 180), (400, 250), 5)  # Corps
    if tentatives == 3:
        pygame.draw.line(fenetre, NOIR, (400, 250), (350, 300), 5)  # Bras gauche
    if tentatives == 2:
        pygame.draw.line(fenetre, NOIR, (400, 250), (450, 300), 5)  # Bras droit
    if tentatives == 1:
        pygame.draw.line(fenetre, NOIR, (400, 300), (350, 350), 5)  # Jambe gauche
    if tentatives == 0:
        pygame.draw.line(fenetre, NOIR, (400, 300), (450, 350), 5)  # Jambe droite

# Boucle principale du jeu
running = True
tentatives = 6  # Nombre de tentatives restantes (affichage du pendu complet)

while running:
    fenetre.fill(BLANC)  # Remplir la fenêtre avec du blanc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner le pendu
    dessiner_pendu(tentatives)

    pygame.display.flip()  # Mettre à jour l'affichage

pygame.quit()
