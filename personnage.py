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

# Initialisation des paramètres du personnage
rect_largeur, rect_hauteur = 50, 50
rect_x, rect_y = 300, 300
vitesse_laterale = 0
vitesse_saut = -10
vitesse_verticale = 0
gravite = 0.5
saut_en_cours = False
sol_y = hauteur - 20

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
obstacles.append(Obstacle(200, sol_y - 150, 150, 25, (255, 0, 0)))  # Un obstacle rouge
obstacles.append(Obstacle(375, sol_y - 100, 150, 25, (255, 0, 0)))  # Un obstacle rouge
obstacles.append(Obstacle(550, sol_y - 50, 150, 25, (255, 0, 0)))  # Un obstacle rouge

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gestion des touches pour les mouvements horizontaux
    touches = pygame.key.get_pressed()
    if touches[pygame.K_a]:
        vitesse_laterale = -5  # Déplacer vers la gauche
    elif touches[pygame.K_d]:
        vitesse_laterale = 5  # Déplacer vers la droite
    else:
        vitesse_laterale = 0  # Arrêter le mouvement latéral

    rect_x += vitesse_laterale

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

    # Mise à jour du rectangle du personnage
    rect_personnage = pygame.Rect(rect_x, rect_y, rect_largeur, rect_hauteur)

    # Vérifier si le personnage est toujours sur un obstacle après la gestion des collisions
    sur_obstacle = False
    for obstacle in obstacles:
        if rect_personnage.colliderect(obstacle.rect) and rect_personnage.bottom == obstacle.rect.top:
            sur_obstacle = True
            break

    # Appliquer la gravité si le personnage n'est pas sur un obstacle
    if not sur_obstacle:
        vitesse_verticale += gravite
    else:
        vitesse_verticale = 0  # Arrêter la gravité si sur un obstacle

    # Assurez-vous que le personnage ne passe pas sous le sol
    if rect_y >= sol_y - rect_hauteur:
        rect_y = sol_y - rect_hauteur
        saut_en_cours = False
        vitesse_verticale = 0

    # Mettre à jour la position verticale du personnage
    rect_y += vitesse_verticale
    rect_personnage = pygame.Rect(rect_x, rect_y, rect_largeur, rect_hauteur)

    # Vérification des collisions avec les obstacles
    for obstacle in obstacles:
        if rect_personnage.colliderect(obstacle.rect):

            diff_top = obstacle.rect.bottom - rect_personnage.top
            diff_bottom = rect_personnage.bottom - obstacle.rect.top
            diff_right = rect_personnage.right - obstacle.rect.left
            diff_left = obstacle.rect.right - rect_personnage.left

            m = min(diff_top, diff_bottom, diff_right, diff_left)

            # Collision par le haut (atterrissage sur l'obstacle)
            if m == diff_bottom:
                rect_y = obstacle.rect.top - rect_hauteur
                vitesse_verticale = 0
                saut_en_cours = False
                sur_obstacle = True

            elif m == diff_right:
                    rect_x = obstacle.rect.left - rect_largeur  # Collision à gauche de l'obstacle

            elif m == diff_left:
                    rect_x = obstacle.rect.right  # Collision à droite de l'obstacle



            elif m == diff_top:
                        rect_y = obstacle.rect.bottom
                        vitesse_verticale = 0

    # Mise à jour de l'écran
    ecran.fill(NOIR)
    pygame.draw.rect(ecran, BLEU, (rect_x, rect_y, rect_largeur, rect_hauteur))
    pygame.draw.rect(ecran, VERT, (0, sol_y, largeur, hauteur - sol_y))  # Dessiner le sol
    for obstacle in obstacles:
        obstacle.afficher(ecran)
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limite à 60 FPS


