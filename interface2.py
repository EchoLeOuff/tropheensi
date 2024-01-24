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
        return "Do(rect={self.rect.topleft})"

class Re(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect

    def __repr__(self):
        return "Re(rect={self.rect.topleft})"

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

# Liste chaînée pour stocker les instances des boutons placés dans la bande noire
placed_buttons_head = None

# Bande noire
black_rect = pygame.Rect(0, resolution[1] - 50, resolution[0], 50)

# Booléen pour savoir si le bouton est en cours de déplacement
moving_button = None

# Booléen pour savoir si l'utilisateur est en train de déplacer un bouton dans la bande noire
moving_button_in_black = None

# Fonction pour insérer un bouton entre deux blocs dans la liste chaînée
def insert_between(new_button, prev_button, next_button, head):
    new_node = Node(new_button)

    if not prev_button:
        new_node.next = head
        return new_node

    new_node.next = next_button
    prev_button.next = new_node

    return head

# Fonction pour ajouter un bouton à la liste chaînée
def add_button_to_list(button, head):
    new_node = Node(button)
    new_node.next = head
    return new_node

# Fonction pour supprimer un bouton de la liste chaînée
def remove_button_from_list(button, head):
    prev = None
    current = head
    while current:
        if current.button == button:
            if prev:
                prev.next = current.next
            else:
                head = current.next
            return head
        prev = current
        current = current.next
    return head

# Fonction pour afficher le contenu de la liste chaînée
def afficher_liste(head):
    current_node = head
    while current_node:
        print(current_node.button)
        current_node = current_node.next

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
                do_instance = Do(do_image, do_image.get_rect())
                do_instance.rect.topleft = mouse_pos
                buttons.append(do_instance)
                moving_button = do_instance  # Définir le bouton en cours de déplacement
                print("Liste buttons:", buttons)

            elif re_button_rect.collidepoint(mouse_pos):
                print("Bouton Ré cliqué")
                # Créer une instance de "Ré" avec l'image associée
                re_instance = Re(re_image, re_image.get_rect())
                re_instance.rect.topleft = mouse_pos
                buttons.append(re_instance)
                moving_button = re_instance  # Définir le bouton en cours de déplacement
                print("Liste buttons:", buttons)

            elif delete_button_rect.collidepoint(mouse_pos):
                print("Bouton Supprimer cliqué")
                deleting = not deleting  # Inverser l'état du mode suppression

            # Vérifier si le clic a eu lieu sur un bouton déjà placé dans la bande noire
            current_node = placed_buttons_head
            while current_node:
                if current_node.button.rect.collidepoint(mouse_pos):
                    print("Bouton placé cliqué")
                    if deleting:
                        # Supprimer le bouton de la liste chaînée
                        placed_buttons_head = remove_button_from_list(current_node.button, placed_buttons_head)
                        print("Bouton supprimé de la bande noire")
                    else:
                        moving_button_in_black = current_node.button  # Définir le bouton en cours de déplacement dans la bande noire
                    break
                current_node = current_node.next

        # Détecter le relâchement du clic de souris
        elif event.type == pygame.MOUSEBUTTONUP:
            if moving_button:
                # Vérifier si le bouton est dans la bande noire
                if black_rect.colliderect(moving_button.rect):
                    # Vérifier si le bouton n'est pas déjà présent dans la liste chaînée
                    is_already_placed = False
                    current_node = placed_buttons_head
                    while current_node:
                        if current_node.button == moving_button:
                            is_already_placed = True
                            break
                        current_node = current_node.next

                    if not is_already_placed:
                        # Trouver la position d'insertion correcte
                        insert_index = None
                        current_node = placed_buttons_head
                        prev_node = None

                        while current_node:
                            if moving_button.rect.centerx < current_node.button.rect.centerx:
                                break

                            prev_node = current_node
                            current_node = current_node.next

                        # Ajouter le bouton à la liste chaînée à la position d'insertion
                        placed_buttons_head = insert_between(
                            moving_button,
                            prev_node.button if prev_node else None,
                            current_node.button if current_node else None,
                            placed_buttons_head
                        )

                        # Redécaler les boutons à droite du bouton déplacé
                        current_x = 200
                        current_node = placed_buttons_head
                        while current_node:
                            current_node.button.rect.topleft = (current_x, black_rect.top)
                            current_x += current_node.button.rect.width + 10
                            current_node = current_node.next

                        print("Liste placed_buttons:")
                        afficher_liste(placed_buttons_head)

                else:
                    # Vérifier si le bouton n'est pas déjà présent dans la liste chaînée
                    is_already_placed = False
                    current_node = placed_buttons_head
                    while current_node:
                        if current_node.button == moving_button:
                            is_already_placed = True
                            break
                        current_node = current_node.next

                    if not is_already_placed:
                        # Trouver la position d'insertion correcte à côté d'un autre bouton
                        insert_index = None
                        current_node = placed_buttons_head
                        prev_node = None

                        while current_node:
                            if moving_button.rect.centerx < current_node.button.rect.centerx:
                                break

                            prev_node = current_node
                            current_node = current_node.next

                        # Ajouter le bouton à la liste chaînée à la position d'insertion
                        placed_buttons_head = insert_between(
                            moving_button,
                            prev_node.button if prev_node else None,
                            current_node.button if current_node else None,
                            placed_buttons_head
                        )

                        # Redécaler les boutons à droite du bouton déplacé
                        current_x = 200
                        current_node = placed_buttons_head
                        while current_node:
                            current_node.button.rect.topleft = (current_x, black_rect.top)
                            current_x += current_node.button.rect.width + 10
                            current_node = current_node.next

                        print("Liste placed_buttons:")
                        afficher_liste(placed_buttons_head)

                moving_button = None  # Réinitialiser le bouton en cours de déplacement

            elif deleting:
                # Supprimer toutes les instances de boutons placés
                current_node = placed_buttons_head
                while current_node:
                    print("Suppression de", current_node.button," de la bande noire")
                    current_node = current_node.next
                placed_buttons_head = None
                print("Toutes les instances de blocs musicaux ont été supprimées")
                deleting = False  # Désactiver le mode suppression
                current_x = 200  # Réinitialiser la position x

            elif deleting:
                # Supprimer toutes les instances de boutons placées
                placed_buttons_head = None
                print("Toutes les instances de blocs musicaux ont été supprimées")
                deleting = False  # Désactiver le mode suppression
                current_x = 10  # Réinitialiser la position x

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
    current_node = placed_buttons_head
    while current_node:
        screen.blit(current_node.button.image, current_node.button.rect.topleft)
        current_node = current_node.next

    # Dessiner le bouton en cours de déplacement
    if moving_button:
        mouse_pos = pygame.mouse.get_pos()
        moving_button.rect.topleft = mouse_pos
        screen.blit(moving_button.image, moving_button.rect.topleft)

    # Dessiner les instances des boutons et suivre le curseur de la souris
    for button in buttons:
        if button != moving_button and button not in placed_buttons_head:
            screen.blit(button.image, button.rect.topleft)

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter la fréquence d'images
    clock.tick(60)
