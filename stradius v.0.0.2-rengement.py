import pygame
import sys

PLAYER_SPEED = 5
JUMP_SPEED = -15
GRAVITY = 1
VERTICAL_SPEED = 0
IS_JUMPING = False

class Mega_class:
    def __init__(self)

class Node:
    def __init__(self, button):
        self.button = button
        self.next = None

class Button:
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()


    def action(self, player):
        pass

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

class Play(Button):
    def __init__(self):
        image = pygame.image.load('assets/play.png')
        image = pygame.transform.scale(image, (50, 50))
        super().__init__(image)



    def action(self, player):
        player.rect.x += PLAYER_SPEED

class Delete(Button):
    def __init__(self):
        image = pygame.image.load('assets/bin.png')
        image = pygame.transform.scale(image, (50, 50))
        super().__init__(image)

    def action(self, linked_list, button):
        linked_list.head = linked_list.remove_button_from_list(button, linked_list.head)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = image
        self.rect = rect

class Player(pygame.sprite.Sprite):
    def __init__(self, speed, jump_speed, gravity):
        image = pygame.image.load('assets/player.png')
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (resolution[0] // 2, resolution[1] - self.rect.height - 50)
        self.speed = speed
        self.jump_speed = jump_speed
        self.gravity = gravity
        self.vertical_speed = VERTICAL_SPEED
        self.is_jumping = IS_JUMPING

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

        if position == 0 or not self.head:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        for _ in range(position - 1):
            if not current.next:
                break
            current = current.next

        new_node.next = current.next
        current.next = new_node

    def remove_button_from_list(self, button, head):
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

    def afficher_liste(self):
        current_node = self.head
        while current_node:
            print("Liste des boutons placés current_node.button")
            current_node = current_node.next

    def executer_actions(self, player):
        current_node = self.head
        while current_node:
            if isinstance(current_node.button, Do):
                player.rect.x += PLAYER_SPEED
            elif isinstance(current_node.button, Re):
                player.rect.y += JUMP_SPEED
            current_node = current_node.next

"""def ajouter_obstacles(obstacles, x, y, nombre):
    for i in range(nombre):
        obstacle = Obstacle(pygame.Surface((30, 30)), pygame.Rect(x, y, 30, 30))
        obstacle.image.fill((0, 0, 255))
        obstacles.add(obstacle)
        x += 150  # Espace entre les obstacles"""

pygame.init()

resolution = (1080, 720)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Mon Super Jeu")

background = pygame.image.load('assets/bg.png')
background = pygame.transform.scale(background, resolution)

BLACK = (0, 0, 0)
"""
do_image = pygame.image.load('assets/do.png')
do_image = pygame.transform.scale(do_image, (50, 50))

re_image = pygame.image.load('assets/re.png')
re_image = pygame.transform.scale(re_image, (50, 50))

delete_image = pygame.image.load('assets/bin.png')
delete_image = pygame.transform.scale(delete_image, (50, 50))

play_image = pygame.image.load('assets/play.png')
play_image = pygame.transform.scale(play_image, (50, 50))

do_button_rect = do_image.get_rect()
do_button_rect.topleft = (resolution[0] - 100, resolution[1] - 150)

re_button_rect = re_image.get_rect()
re_button_rect.topleft = (resolution[0] - 100, resolution[1] - 80)

delete_button_rect = delete_image.get_rect()
delete_button_rect.topleft = (resolution[0] - 100, resolution[1] - 220)

play_button_rect = play_image.get_rect()
play_button_rect.topleft = (resolution[0] - 100, resolution[1] - 290)
"""
buttons = []
obstacles = pygame.sprite.Group()

placed_buttons_head = None

#ajouter_obstacles(obstacles, 300, resolution[1] - 80, 3)

black_rect = pygame.Rect(0, resolution[1] - 50, resolution[0], 50)

moving_button = None
deleting = False
display_list = False
is_playing = False

liste_chainee = ListeChainee()
player = Player(PLAYER_SPEED, JUMP_SPEED, GRAVITY)
do = Do()
re = Re()
play = Play()
delete = Delete()

mega_classe = Mega_classe()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if do_button_rect.collidepoint(mouse_pos):
                print("Bouton Do cliqué")
                do_instance = Do(do_image, do_image.get_rect())
                do_instance.rect.topleft = mouse_pos
                buttons.append(do_instance)
                moving_button = do_instance

            elif re_button_rect.collidepoint(mouse_pos):
                print("Bouton Ré cliqué")
                re_instance = Re(re_image, re_image.get_rect())
                re_instance.rect.topleft = mouse_pos
                buttons.append(re_instance)
                moving_button = re_instance

            elif delete_button_rect.collidepoint(mouse_pos):
                print("Bouton Supprimer cliqué")
                deleting = not deleting

            elif play_button_rect.collidepoint(mouse_pos):
                print("Bouton Play cliqué")
                liste_chainee.executer_actions(player)
                is_playing = True

            current_node = placed_buttons_head
            while current_node:
                if current_node.button.rect.collidepoint(mouse_pos):
                    print("Bouton placé cliqué")
                    if deleting:
                        placed_buttons_head = liste_chainee.remove_button_from_list(current_node.button, placed_buttons_head)
                        print("Bouton supprimé de la bande noire")
                    else:
                        moving_button = current_node.button
                    break
                current_node = current_node.next

        elif event.type == pygame.MOUSEBUTTONUP:
            if moving_button:
                if black_rect.colliderect(moving_button.rect):
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
        player.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT])
    else:
        player.update(False, False)

    if keys[pygame.K_SPACE]:
        player.jump()

    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)

    screen.blit(do.image, do.rect.topleft)
    screen.blit(re.image, re.rect.topleft)
    screen.blit(delete.image, delete.rect.topleft)
    screen.blit(play.image, play.rect.topleft)

    pygame.draw.rect(screen, BLACK, black_rect)

    current_node = placed_buttons_head
    while current_node:
        screen.blit(current_node.button.image, current_node.button.rect.topleft)
        current_node = current_node.next

    for obstacle in obstacles:
        screen.blit(obstacle.image, obstacle.rect.topleft)

    if moving_button:
        mouse_pos = pygame.mouse.get_pos()
        moving_button.rect.topleft = mouse_pos
        screen.blit(moving_button.image, moving_button.rect.topleft)

    for button in buttons:
        if button != moving_button and button not in placed_buttons_head:
            screen.blit(button.image, button.rect.topleft)

    pygame.display.flip()

    if display_list:
        liste_chainee.afficher_liste()
        display_list = False

    clock.tick(60)
