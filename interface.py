import pygame
import sys

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
player_image = pygame.transform.scale(player_image, (50, 50))  # Ajuster la taille du joueur
player_rect = player_image.get_rect()

# Définir les propriétés du joueur
player_rect.center = (resolution[0] // 2, resolution[1] - player_rect.height - 50)  # 50 pixels au-dessus du bas

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

# Liste pour stocker les instances des boutons placés dans la bande noire
placed_buttons = []

# Bande noire
black_rect = pygame.Rect(0, resolution[1] - 50, resolution[0], 50)

# Booléen pour savoir si le bouton est en cours de déplacement
moving_button = None

# Position initiale x pour les boutons dans la bande noire
current_x = 10

# Booléen pour savoir si le bouton est en cours de suppression
deleting = False

# Booléen pour savoir si un bouton est en cours de redimensionnement
resizing_button = None

# Boucle de jeu
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Détecter les clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Vérifier si le clic a eu lieu sur l'un des boutons
            if do_button_rect.collidepoint(mouse_pos):
                print("Bouton Do cliqué")
                # Créer une instance de "Do" avec l'image associée
                do_instance = pygame.sprite.Sprite()
                do_instance.image = do_image
                do_instance.rect = do_instance.image.get_rect()
                do_instance.rect.topleft = mouse_pos
                buttons.append(do_instance)
                moving_button = do_instance  # Définir le bouton en cours de déplacement

            elif re_button_rect.collidepoint(mouse_pos):
                print("Bouton Ré cliqué")
                # Créer une instance de "Ré" avec l'image associée
                re_instance = pygame.sprite.Sprite()
                re_instance.image = re_image
                re_instance.rect = re_instance.image.get_rect()
                re_instance.rect.topleft = mouse_pos
                buttons.append(re_instance)
                moving_button = re_instance  # Définir le bouton en cours de déplacement

            elif delete_button_rect.collidepoint(mouse_pos):
                print("Bouton Supprimer cliqué")
                deleting = True  # Activer le mode suppression

            # Vérifier si le clic a eu lieu sur un bouton déjà placé dans la bande noire
            for button in placed_buttons:
                if button.rect.collidepoint(mouse_pos):
                    print("Bouton placé cliqué")
                    moving_button = button  # Définir le bouton en cours de déplacement

        # Détecter le relâchement du clic de souris
        elif event.type == pygame.MOUSEBUTTONUP:
            if moving_button:
                # Vérifier si le bouton est dans la bande noire
                if black_rect.colliderect(moving_button.rect):
                    # Trouver la position d'insertion correcte
                    insert_index = None
                    for i, button in enumerate(placed_buttons):
                        if moving_button.rect.centerx < button.rect.centerx:
                            insert_index = i
                            break
                    if insert_index is not None:
                        placed_buttons.insert(insert_index, moving_button)
                    else:
                        placed_buttons.append(moving_button)

                    # Redécaler les boutons à droite du bouton déplacé
                    current_x = 200
                    for i in range(len(placed_buttons)):
                        placed_buttons[i].rect.topleft = (current_x, black_rect.top)
                        current_x += placed_buttons[i].rect.width + 10

                    # Mettre à jour la position x courante
                    current_x = current_x + 10

                else:
                    print("Le bouton doit être placé dans la bande noire")
                    moving_button.rect.topleft = (current_x, black_rect.top)  # Retourner à la position précédente

                # Supprimer le bouton de la liste buttons s'il appartient à cette liste
                if moving_button in buttons:
                    buttons.remove(moving_button)

                moving_button = None  # Réinitialiser le bouton en cours de déplacement

            elif deleting:
                # Supprimer toutes les instances de boutons placées
                for button in placed_buttons:
                    # Supprimer le bouton de la liste buttons s'il appartient à cette liste
                    if button in buttons:
                        buttons.remove(button)
                placed_buttons = []
                print("Toutes les instances de blocs musicaux ont été supprimées")
                deleting = False  # Désactiver le mode suppression
                current_x = 10  # Réinitialiser la position x

            elif resizing_button:
                resizing_button = None  # Désactiver le mode redimensionnement

    # Déplacement du joueur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < resolution[0]:
        player_rect.x += player_speed

    # Saut du joueur
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        player_rect.y += jump_speed
        jump_speed += gravity
        if player_rect.y > resolution[1] - player_rect.height - 50:  # 50 pixels au-dessus du bas
            is_jumping = False
            jump_speed = -10
            player_rect.y = resolution[1] - player_rect.height - 50

    # Effacer l'écran
    screen.blit(background, (0, 0))

    # Dessiner le joueur
    screen.blit(player_image, player_rect)

    # Dessiner les boutons
    screen.blit(do_image, do_button_rect.topleft)
    screen.blit(re_image, re_button_rect.topleft)
    screen.blit(delete_image, delete_button_rect.topleft)  # Dessiner l'image du bouton Supprimer

    # Dessiner la bande noire en bas
    pygame.draw.rect(screen, BLACK, black_rect)

    # Dessiner les instances des boutons dans la bande noire
    for button in placed_buttons:
        screen.blit(button.image, button.rect.topleft)

    # Dessiner le bouton en cours de déplacement
    if moving_button:
        mouse_pos = pygame.mouse.get_pos()
        moving_button.rect.topleft = mouse_pos
        screen.blit(moving_button.image, moving_button.rect.topleft)

    # Dessiner les instances des boutons et suivre le curseur de la souris
    for button in buttons:
        if button != moving_button and button not in placed_buttons:
            screen.blit(button.image, button.rect.topleft)

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter la fréquence d'images
    clock.tick(60)
