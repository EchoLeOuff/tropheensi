import pygame
import sys
import os

class Block:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image_path = image_path
        self.load_image()
        self.resize_image()

    def load_image(self):
        self.image = pygame.image.load(self.image_path)

    def resize_image(self):
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))

    def update_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0]:  # Vérifier si le bouton gauche est enfoncé
            if self.x - self.image.get_width() // 2 < mouse_x < self.x + self.image.get_width() // 2 and \
               self.y - self.image.get_height() // 2 < mouse_y < self.y + self.image.get_height() // 2:
                # Calculer la nouvelle position du bloc en fonction de la position de la souris
                direction_x = mouse_x - self.x
                direction_y = mouse_y - self.y
                distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
                if distance > 0:
                    self.x += int(speed * direction_x / distance)
                    self.y += int(speed * direction_y / distance)

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blocs avec images")

# Création des blocs avec leurs images
block1 = Block(100, 100, os.path.join("U:", "Documents", "projetnsi","blocdo.png"))
block2 = Block(200, 200, os.path.join("U:", "Documents", "projetnsi","blocre.png"))
block3 = Block(300, 300, os.path.join("U:", "Documents", "projetnsi","blocmi.png"))
block4 = Block(400, 400, os.path.join("U:", "Documents", "projetnsi","blocfa.png"))

blocks = [block1, block2, block3, block4]

# Vitesse de déplacement du bloc
speed = 5

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mettre à jour la position des blocs en fonction de la souris
    for block in blocks:
        block.update_position()

    # Effacer l'écran
    screen.fill((255, 255, 255))

    # Dessiner les blocs avec les images
    for block in blocks:
        screen.blit(block.image, (block.x - block.image.get_width() // 2, block.y - block.image.get_height() // 2))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence d'images
    pygame.time.Clock().tick(60)
