import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 800, 600
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption('Jeu Pygame - Rectangle')

# Couleurs
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)

# Paramètres du rectangle
rect_largeur, rect_hauteur = 50, 50
rect_x, rect_y = largeur // 2, hauteur // 2
vitesse = 5
vitesse_saut = -10  # Vitesse négative pour aller vers le haut
gravite = 1
saut_en_cours = False
sol_y = hauteur - 70  # Position du sol

class Obstacle:
    def __init__(self, x, y, largeur, hauteur, couleur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.rect = pygame.Rect(x, y, largeur, hauteur)

    def afficher(self, ecran):
        pygame.draw.rect(ecran, self.couleur, self.rect)

obstacles = []
obstacles.append(Obstacle(300, sol_y - 50, 150, 25, (255, 0, 0)))  # Un obstacle rouge

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gestion des touches
    touches = pygame.key.get_pressed()
    if touches[pygame.K_a]:
        rect_x -= vitesse
    if touches[pygame.K_d]:
        rect_x += vitesse

    # Saut
    if not saut_en_cours and touches[pygame.K_SPACE]:
        saut_en_cours = True
        vitesse_verticale = vitesse_saut

    # Collision avec les bordures de l'écran
    if rect_x < 0:  # Gauche
        rect_x = 0
    if rect_x > largeur - rect_largeur:  # Droite
        rect_x = largeur - rect_largeur
    if rect_y < 0:  # Haut
        rect_y = 0
    if rect_y > sol_y - rect_hauteur:  # Bas (le sol)
        rect_y = sol_y - rect_hauteur
        saut_en_cours = False

    # Gravité
    if saut_en_cours:
        rect_y += vitesse_verticale
        vitesse_verticale += gravite
        if rect_y >= sol_y - rect_hauteur:  # Collision avec le sol
            rect_y = sol_y - rect_hauteur
            saut_en_cours = False

    # Mise à jour de l'écran
    ecran.fill(NOIR)
    pygame.draw.rect(ecran, BLEU, (rect_x, rect_y, rect_largeur, rect_hauteur))
    pygame.draw.rect(ecran, VERT, (0, sol_y, largeur, hauteur - sol_y))  # Dessiner le sol
    for obstacle in obstacles:
        obstacle.afficher(ecran)
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limite à 60 FPS


