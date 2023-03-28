import os
import pygame
from player import Player

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def game_loop(screen, clock, running, dt):
    player1 = Player('sword', "images/default.png", 'player1', screen,
                     pygame.Vector2(screen.get_width() / 1.5, 510), "red")
    player2 = Player('sword', 'images/default.png', 'player2', screen,
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
                    player2.update_image("images/reverse.png")
                    player2.counter = 0
                elif player2.last_action == "running-right":
                    player2.update_image("images/default.png")
                    player2.counter = 0
                if player1.last_action == "running-left":
                    player1.update_image("images/reverse.png")
                    player1.counter = 0
                elif player1.last_action == "running-right":
                    player1.update_image("images/default.png")
                    player1.counter = 0



        player1.show_player()
        player2.show_player()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player1.last_action = "running-left"
            player1.counter += 1
            player1.run_left()
            player1.move_left(dt)
        if keys[pygame.K_d]:
            player1.last_action = "running-right"
            player1.counter += 1
            player1.run_right()
            player1.move_right(dt)
        if keys[pygame.K_RIGHT]:
            player2.last_action = "running-right"
            player2.counter += 1
            player2.run_right()
            player2.move_right(dt)
        if keys[pygame.K_LEFT]:
            player2.last_action = "running-left"
            player2.counter += 1
            player2.run_left()
            player2.move_left(dt)

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
