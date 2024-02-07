import pygame
import sys

PLAYER_SPEED = 5
JUMP_SPEED = -15
GRAVITY = 1
VERTICAL_SPEED = 5
IS_JUMPING = False

class Mega_class:
    def __init__(self):
        pass

class Node:
    def __init__(self, button):
        self.button = button
        self.next = None

class Button_fixe(pygame.sprite.Sprite):
    def __init__(self, img, pos = None):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(img)
        image = pygame.transform.scale(image, (50, 50))
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.pos_x = image.get_rect()[0]
        self.pos_y = image.get_rect()[1]

    def affichage(self):
        if self.pos is not None:
            screen.blit(self.image, self.pos)

class Button(Button_fixe, pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()

class Do(Button):
    def __init__(self):
        image = pygame.image.load('assets/do.png')
        image = pygame.transform.scale(image, (50, 50))
        super().__init__(image)

    def action(self, player):
        player.rect.x += PLAYER_SPEED

    def __repr__(self):
        return "Do(rect={self.rect.topleft})"

class Re(Button):
    def __init__(self):
        image = pygame.image.load('assets/re.png')
        image = pygame.transform.scale(image, (50, 50))
        super().__init__(image)


    def action(self, player):
        player.rect.y += JUMP_SPEED

    def __repr__(self):
        return "Re(rect={self.rect.topleft})"

class Player(pygame.sprite.Sprite):
    def __init__(self, speed, jump_speed, gravity):
        image = pygame.image.load('assets/player.png')
        size = (50, 50)
        image = pygame.transform.scale(image, size)
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (resolution[0] // 2, resolution[1] - self.rect.height - 50)
        self.speed = speed
        self.jump_speed = jump_speed
        self.gravity = gravity
        self.vertical_speed = VERTICAL_SPEED
        self.is_jumping = IS_JUMPING
        self.pos_x = self.rect[0]
        self.pos_y = self.rect[1]

    def jump(self):
        if not self.is_jumping:
            self.vertical_speed = self.jump_speed
            self.is_jumping = True

    def update(self, move_left, move_right):
        if move_left:
            self.rect.x -= self.speed
        if move_right:
            self.rect.x += self.speed

        self.vertical_speed += self.gravity
        self.rect.y += self.vertical_speed

        if self.rect.y > resolution[1] - self.rect.height - 50:
            self.rect.y = resolution[1] - self.rect.height - 50
            self.vertical_speed = 0
            self.is_jumping = False

class ListeChainee:
    def __init__(self):
        self.head = None

    def ajouter_dans_la_liste(self, button, position):
        new_node = Node(button)

        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def insert_between(self, button_to_insert, button_before, button_after):
        # Créer un nouveau nœud avec le bouton à insérer
        new_node = Node(button_to_insert)

        # Parcourir la liste pour trouver le nœud correspondant au bouton avant
        current = self.head
        while current:
            if current.button == button_before:
                break
            current = current.next
        if not current:
            return  # Si le bouton avant n'est pas dans la liste, ne rien faire

        # Insérer le nouveau nœud après le nœud correspondant au bouton avant
        new_node.next = current.next
        current.next = new_node

    def remove_button_from_list(self):
        self.head = None

    def afficher_liste(self):
        current_node = self.head
        while current_node:
            print("Liste des boutons placés ",current_node.button)
            current_node = current_node.next

    def executer_actions(self, player):
        current_node = self.head
        while current_node:
            if isinstance(current_node.button, Do):
                player.rect.x += PLAYER_SPEED
            elif isinstance(current_node.button, Re):
                player.rect.y += JUMP_SPEED
            current_node = current_node.next

    def affichage(self):
        current_node = self.head
        current_x = 200  # Position horizontale de départ des boutons dans la bande noire
        while current_node:
            current_x += current_node.button.rect.width + 10
            screen.blit(current_node.button.image, (current_x, black_rect.top))
            current_node = current_node.next



class Bg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/bg.png').convert()
        self.image = image
        self.pos_x = 0
        self.pos_y = 0

def actualiser():
    # Actualiser la position du joueur en fonction de sa vitesse
    PLAYER.rect.y += PLAYER.vertical_speed
    # Actualiser la position des boutons en fonction de leurs positions
    DO.rect.topleft = DO.pos
    RE.rect.topleft = RE.pos
    PLAY.rect.topleft = PLAY.pos
    DELETE.rect.topleft = DELETE.pos



pygame.init()

resolution = (1080, 720)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Mon Super Jeu")

BLACK = (0, 0, 0)

buttons = []
obstacles = pygame.sprite.Group()

placed_buttons_head = None

black_rect = pygame.Rect(0, 670, 1080, 720)
print(black_rect)


moving_button = None
deleting = False
display_list = False
is_playing = False
is_already_placed = None

liste_chainee = ListeChainee()
PLAYER = Player(PLAYER_SPEED, JUMP_SPEED, GRAVITY)
DO = Button_fixe('assets/do.png',(980, 600))
RE = Button_fixe('assets/re.png',(980, 540))
PLAY = Button_fixe('assets/play.png',(980, 480))
DELETE = Button_fixe('assets/bin.png',(980,420))
BG = Bg()

#mega_classe = Mega_classe()
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if DO.rect.collidepoint(mouse_pos):
                print("Bouton Do cliqué")
                do_instance = Do()
                do_instance.rect.topleft = mouse_pos
                buttons.append(do_instance)
                moving_button = do_instance

            elif RE.rect.collidepoint(mouse_pos):
                print("Bouton Ré cliqué")
                re_instance = Re()
                re_instance.rect.topleft = mouse_pos
                buttons.append(re_instance)
                moving_button = re_instance

            elif DELETE.rect.collidepoint(mouse_pos):
                print("Bouton Supprimer cliqué")
                liste_chainee.remove_button_from_list()

            elif PLAY.rect.collidepoint(mouse_pos):
                print("Bouton Play cliqué")
                liste_chainee.executer_actions(PLAYER)
                is_playing = True


        elif event.type == pygame.MOUSEBUTTONUP:
            if moving_button:
                if black_rect.colliderect(moving_button.rect):
                    current_node = placed_buttons_head
                    while current_node:
                        if current_node.button == moving_button:
                            is_already_placed = True
                            break
                        current_node = current_node.next

                    if not is_already_placed:
                        insert_index = 0
                        current_node = placed_buttons_head
                        while current_node:
                            if moving_button.rect.centerx < current_node.button.rect.centerx:
                                break
                            current_node = current_node.next
                            insert_index += 1

                        liste_chainee.ajouter_dans_la_liste(moving_button, insert_index)

                        current_x = 200
                        current_node = placed_buttons_head
                        while current_node:
                            current_node.button.rect.topleft = (current_x, black_rect.top)
                            current_x += current_node.button.rect.width + 10
                            current_node = current_node.next

                        display_list = True

                else:
                    is_already_placed = False
                    current_node = placed_buttons_head
                    while current_node:
                        if current_node.button == moving_button:
                            is_already_placed = True
                            break
                        current_node = current_node.next

                    if not is_already_placed:
                        insert_index = 0
                        current_node = placed_buttons_head
                        while current_node:
                            if moving_button.rect.centerx < current_node.button.rect.centerx:
                                break
                            current_node = current_node.next
                            insert_index += 1

                        liste_chainee.ajouter_dans_la_liste(moving_button, insert_index)

                        current_x = 200
                        current_node = placed_buttons_head
                        while current_node:
                            current_node.button.rect.topleft = (current_x, black_rect.top)
                            current_x += current_node.button.rect.width + 10
                            current_node = current_node.next

                        display_list = True

                if moving_button in buttons:
                    buttons.remove(moving_button)

                moving_button = None

            elif deleting:
                placed_buttons_head = None
                print("Toutes les instances de blocs musicaux ont été supprimées")
                deleting = False
                current_x = 10

    keys = pygame.key.get_pressed()

    if not is_playing:
        PLAYER.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT])
    else:
        PLAYER.update(False, False)

    if keys[pygame.K_SPACE]:
        PLAYER.jump()

    actualiser()
    screen.blit(BG.image, (BG.pos_x, BG.pos_y))
    DO.affichage()
    RE.affichage()
    PLAY.affichage()
    DELETE.affichage()
    pygame.draw.rect(screen, BLACK, black_rect)
    liste_chainee.affichage()
    screen.blit(PLAYER.image, PLAYER.rect)



    # Dessine les boutons en mouvement
    if moving_button:
        mouse_pos = pygame.mouse.get_pos()
        moving_button.rect.topleft = mouse_pos
        screen.blit(moving_button.image, moving_button.rect.topleft)

    pygame.display.flip()

    if display_list:
        liste_chainee.afficher_liste()
        display_list = False

    clock.tick(60)
