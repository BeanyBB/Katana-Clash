import os
import pygame
from player import Player

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def check_player_jump(Player):
    if Player.is_jump:
        if Player.player_pos.y == 510 and Player.jump_count != 0:
            Player.is_jump = False
            Player.mass = 1
            Player.vel = 15
            Player.jump_count = 0
        else:
            Player.jump_count += 1
            if Player.vel < 0:
                Player.mass = -1
            force = ((1/2) * Player.mass * Player.vel**2)*.4
            Player.player_pos.y -= force
            Player.vel = Player.vel - .5
        Player.do_jump_animation()

def check_player_attack(Player):
    if Player.attacking:
        Player.attack_count += 1
        if Player.attack_count < 15:
            if Player.facing == 'right': Player.update_image(f"images/{Player.folder}/attack/attack1.png")
            else: Player.update_image(f"images/{Player.folder}/attack/attack1rev.png")
        elif Player.attack_count <= 30:
            if Player.facing == 'right': Player.update_image(f"images/{Player.folder}/attack/attack2.png")
            else: Player.update_image(f"images/{Player.folder}/attack/attack2rev.png")
        elif Player.attack_count <= 45:
            if Player.facing == 'right': Player.update_image(f"images/{Player.folder}/attack/attack3.png")
            else: Player.update_image(f"images/{Player.folder}/attack/attack3rev.png")
        else:
            if Player.facing == 'right': Player.update_image(f"images/{Player.folder}/default.png")
            else: Player.update_image(f"images/{Player.folder}/reverse.png")
            Player.attacking = False
            Player.attack_count = 0



def game_loop(screen, clock, running, dt):
    player1 = Player('sword', "commander", 'player1', screen,
                     pygame.Vector2(screen.get_width() / 1.5, 510), "red")
    player2 = Player('sword', 'samurai', 'player2', screen,
                     pygame.Vector2(screen.get_width() / 3, 510), "blue")

    bg = Background("images/background.jpg", [0,0])
    ground = Background("images/ground.png", [0,230])

    while running:
        screen.fill([255, 255, 255])
        screen.blit(bg.image, bg.rect)
        screen.blit(ground.image, ground.rect)

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if player2.last_action == "running-left":
                    player2.update_image(f"images/{player2.folder}/reverse.png")
                    player2.counter = 0
                elif player2.last_action == "running-right":
                    player2.update_image(f"images/{player2.folder}/default.png")
                    player2.counter = 0
                if player1.last_action == "running-left":
                    player1.update_image(f"images/{player1.folder}/reverse.png")
                    player1.counter = 0
                elif player1.last_action == "running-right":
                    player1.update_image(f"images/{player1.folder}/default.png")
                    player1.counter = 0





        player1.show_player()
        player2.show_player()

        check_player_jump(player1)
        check_player_jump(player2)

        check_player_attack(player1)
        check_player_attack(player2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if player1.attacking == False or player1.is_jump:
                player1.last_action = "running-left"
                player1.counter += 1
                player1.run_left()
                player1.move_left(dt)
        if keys[pygame.K_d]:
            if player1.attacking == False or player1.is_jump:
                player1.last_action = "running-right"
                player1.counter += 1
                player1.run_right()
                player1.move_right(dt)
        if keys[pygame.K_l]:
            if player2.attacking == False or player2.is_jump:
                player2.last_action = "running-right"
                player2.counter += 1
                player2.run_right()
                player2.move_right(dt)
        if keys[pygame.K_j]:
            if player2.attacking == False or player2.is_jump:
                player2.last_action = "running-left"
                player2.counter += 1
                player2.run_left()
                player2.move_left(dt)
        if keys[pygame.K_w]:
            player1.jump()
        if keys[pygame.K_i]:
            player2.jump()
        if keys[pygame.K_k]:
            player2.attack()
        if keys[pygame.K_s]:
            player1.attack()

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    game_loop(screen, clock, running, dt)


if __name__ == '__main__':
    main()
