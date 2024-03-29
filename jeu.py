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

# Charger l'image pour le bouton "Play"
play_image = pygame.image.load('assets/play.png')
play_image = pygame.transform.scale(play_image, (50, 50))

# Position des boutons
do_button_rect = do_image.get_rect()
do_button_rect.topleft = (resolution[0] - 100, resolution[1] - 150)

re_button_rect = re_image.get_rect()
re_button_rect.topleft = (resolution[0] - 100, resolution[1] - 80)

delete_button_rect = delete_image.get_rect()
delete_button_rect.topleft = (resolution[0] - 100, resolution[1] - 220)

play_button_rect = play_image.get_rect()
play_button_rect.topleft = (resolution[0] - 100, resolution[1] - 290)

# Liste pour stocker les instances des boutons
buttons = []

# Liste pour stocker les instances des boutons placés dans la bande noire
placed_buttons = []

# Bande noire
black_rect = pygame.Rect(0, resolution[1] - 50, resolution[0], 50)

# Booléen pour savoir si le bouton est en cours de déplacement
moving_button = None

# Position initiale x pour les boutons dans la bande noire
current_x = 200

# Booléen pour savoir si le bouton est en cours de suppression
deleting = False

# Booléen pour savoir si un bouton est en cours de redimensionnement
resizing_button = None

# Boucle de jeu
clock = pygame.time.Clock()

# Nouvelle variable pour suivre le déplacement du personnage
movement_distance = 0

# Booléen pour savoir si le bouton "Play" a été cliqué
play_button_clicked = False

# Booléen pour savoir si l'édition des boutons est activée
editing_enabled = True

# Boucle de jeu
clock = pygame.time.Clock()

# Variable pour suivre l'index du bloc en cours d'exécution
n = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Détecter les clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Vérifier si le bouton "Play" est cliqué
            if play_button_rect.collidepoint(mouse_pos):
                print("Bouton Play cliqué")
                play_button_clicked = not play_button_clicked  # Inverser l'état du bouton "Play"

                # Si le mode "Play" est activé, désactiver l'édition des boutons
                if play_button_clicked:
                    moving_button = None
                    deleting = False
                    resizing_button = None
                    editing_enabled = False
                else:
                    editing_enabled = True  # Réactiver l'édition des boutons lorsque le mode "Play" est désactivé

                # Réinitialiser l'index du bloc en cours d'exécution
                n = 0

            # Si l'édition des boutons est activée, gérer les clics sur les boutons normalement
            if editing_enabled:
                if do_button_rect.collidepoint(mouse_pos):
                    print("Bouton Do cliqué")
                    do_instance = pygame.sprite.Sprite()
                    do_instance.image = do_image
                    do_instance.rect = do_instance.image.get_rect()
                    do_instance.rect.topleft = mouse_pos
                    buttons.append(do_instance)
                    moving_button = do_instance

                elif re_button_rect.collidepoint(mouse_pos):
                    print("Bouton Ré cliqué")
                    re_instance = pygame.sprite.Sprite()
                    re_instance.image = re_image
                    re_instance.rect = re_instance.image.get_rect()
                    re_instance.rect.topleft = mouse_pos
                    buttons.append(re_instance)
                    moving_button = re_instance

                elif delete_button_rect.collidepoint(mouse_pos):
                    print("Bouton Supprimer cliqué")
                    deleting = True

        # Détecter le relâchement du clic de souris
        elif event.type == pygame.MOUSEBUTTONUP:
            if moving_button:
                if black_rect.colliderect(moving_button.rect):
                    if moving_button in placed_buttons:
                        placed_buttons.remove(moving_button)
                    placed_buttons.append(moving_button)
                    moving_button.rect.topleft = (current_x, black_rect.top)
                    current_x += moving_button.rect.width + 10
                else:
                    print("Le bouton doit être placé dans la bande noire")
                    moving_button.rect.topleft = (current_x, black_rect.top)
                moving_button = None

            elif deleting:
                for button in placed_buttons:
                    buttons.remove(button)
                placed_buttons = []
                print("Toutes les instances de blocs musicaux ont été supprimées")
                deleting = False
                current_x = 200

            elif resizing_button:
                resizing_button = None

    for button in placed_buttons:
        if play_button_clicked:
            if n < len(placed_buttons):
                current_button = placed_buttons[n]

                if current_button.image == do_image:
                    movement_distance += player_speed
                    player_rect.x += player_speed
                    if movement_distance >= 100:
                        movement_distance -= 100
                        n += 1
                elif current_button.image == re_image:
                    movement_distance -= player_speed
                    player_rect.x -= player_speed
                    if movement_distance <= -100:
                        movement_distance += 100
                        n += 1

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
        if player_rect.y > resolution[1] - player_rect.height - 50:
            is_jumping = False
            jump_speed = -10
            player_rect.y = resolution[1] - player_rect.height - 50

    screen.blit(background, (0, 0))

    # Dessiner le joueur
    screen.blit(player_image, player_rect)

    # Dessiner les boutons
    screen.blit(do_image, do_button_rect.topleft)
    screen.blit(re_image, re_button_rect.topleft)
    screen.blit(delete_image, delete_button_rect.topleft)
    screen.blit(play_image, play_button_rect.topleft)

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

    # Dessiner le rectangle d'état sous le bouton "Play"
    pygame.draw.rect(screen, (0, 255, 0) if play_button_clicked else (255, 0, 0), play_button_rect)

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter la fréquence d'images
    clock.tick(60)
