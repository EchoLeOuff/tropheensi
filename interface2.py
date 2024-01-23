import pygame
import sys

class Node:
    def __init__(self, button):
        self.button = button
        self.next = None

class Do(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect

    def __repr__(self):
        return print("Do(rect={self.rect.topleft})")

class Re(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect

    def __repr__(self):
        return print("Re(rect={self.rect.topleft})")

# Initialisation de Pygame
pygame.init()

# Définir la résolution de l'écran
resolution = (1080, 720)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Mon Super Jeu")

# Charger le fond
background = pygame.image.load('assets/bg.png')
background = pygame.transform.scale(background, resolution)

# Charger le joueur (sprite)
player_image = pygame.image.load('assets/player.png')
player_image = pygame.transform.scale(player_image, (50, 50))
player_rect = player_image.get_rect()
player_rect.center = (resolution[0] // 2, resolution[1] - player_rect.height - 50)

# Définir la vitesse du joueur et la gravité pour le saut
player_speed = 5
jump_speed = -10
gravity = 1
is_jumping = False

# Couleur noire
BLACK = (0, 0, 0)

# Charger les images pour les boutons "Do" et "Ré"
do_image = pygame.image.load('assets/do.png')
do_image = pygame.transform.scale(do_image, (50, 50))

re_image = pygame.image.load('assets/re.png')
re_image = pygame.transform.scale(re_image, (50, 50))

# Charger l'image pour le bouton "Supprimer"
delete_image = pygame.image.load('assets/bin.png')
delete_image = pygame.transform.scale(delete_image, (50, 50))

# Position des boutons
do_button_rect = do_image.get_rect()
do_button_rect.topleft = (resolution[0] - 100, resolution[1] - 150)

re_button_rect = re_image.get_rect()
re_button_rect.topleft = (resolution[0] - 100, resolution[1] - 80)

delete_button_rect = delete_image.get_rect()
delete_button_rect.topleft = (resolution[0] - 100, resolution[1] - 220)

# Liste pour stocker les instances des boutons
buttons = []

# Liste chaînée pour stocker les instances des boutons placés dans la bande noire
placed_buttons_head = None

# Booléen pour savoir si le bouton est en cours de déplacement
moving_button = None

# Booléen pour savoir si le bouton est en cours de suppression
deleting = False

# Boucle de jeu
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Effacer l'écran
    screen.blit(background, (0, 0))

    # Dessiner le joueur
    screen.blit(player_image, player_rect)

    # Dessiner les boutons
    screen.blit(do_image, do_button_rect.topleft)
    screen.blit(re_image, re_button_rect.topleft)
    screen.blit(delete_image, delete_button_rect.topleft)

    # Dessiner la bande noire en bas
    pygame.draw.rect(screen, BLACK, (0, resolution[1] - 50, resolution[0], 50))

    # Dessiner les instances des boutons dans la bande noire
    current_node = placed_buttons_head
    while current_node:
        screen.blit(current_node.button.image, current_node.button.rect.topleft)
        current_node = current_node.next

    # Dessiner le bouton en cours de déplacement
    if moving_button:
        mouse_pos = pygame.mouse.get_pos()
        moving_button.rect.topleft = mouse_pos
        screen.blit(moving_button.image, moving_button.rect.topleft)

    # Dessiner les instances des boutons
    for button in buttons:
        if button != moving_button and button not in placed_buttons_head:
            screen.blit(button.image, button.rect.topleft)

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter la fréquence d'images
    clock.tick(60)
