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
        print(Player.rect.y)
        if Player.player_pos.y == Player.origin and Player.jump_count != 0:
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


def game_loop(screen, clock, running, dt):
    player1 = Player('sword', "commander", 'player1', screen,
                     pygame.Vector2(screen.get_width() / 3, 372), "red", [screen.get_width() / 3, 372])
    player2 = Player('sword', 'samurai', 'player2', screen,
                     pygame.Vector2(screen.get_width() / 1.5, 430), "blue", [screen.get_width() / 1.5, 430])
    display1 = Player('sword', "commander", 'display1', screen,
                     pygame.Vector2(0, 372), "red", [0,372])
    display2 = Player('sword', 'samurai', 'display2', screen,
                      pygame.Vector2(1215, 430), "blue", [1215,430])
    all_players = [player1, player2]
    bg = Background("images/background.png", [0,0])
    main_menu = Background("images/mainMenu.jpg", [0,0])
    green = (0, 255, 0)
    blue = (0, 0, 128)
    font = pygame.font.Font('freesansbold.ttf', 32)
    game_on = False
    game_over_count = 0
    logo = pygame.image.load("images/logo.png")
    space = pygame.image.load("images/space.png")


    while running:
        if game_on:
            screen.blit(bg.image, bg.rect)
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    for player in all_players:
                        if player.last_action == "running-left" and player.attacking == False:
                            player.update_image(f"images/{player.folder}/reverse.png")
                            player.counter = 0
                        elif player.last_action == "running-right" and player.attacking == False:
                            player.update_image(f"images/{player.folder}/default.png")
                            player.counter = 0


            text = font.render(f'player1: {player1.health}   player2: {player2.health}', True, green, blue)
            textRect = text.get_rect()
            textRect.center = (1366/2, 50)

            for player in all_players:
                player.show_player()
                player.check_player_jump()
                player.check_player_attack()
                if player.health <= 0:
                    game_over_count += 1
                    if player == player2: winner = 'player1'
                    else: winner = 'player2'
                    text = font.render(f'GAME OVER     WINNER --> {winner}', True, green, blue)
                    if game_over_count == 300:
                        game_on = False

            screen.blit(text, textRect)

            player1.check_player_hit(player2)
            player2.check_player_hit(player1)

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
                player2.attack(player1)
            if keys[pygame.K_s]:
                player1.attack(player2)


        else:
            screen.blit(main_menu.image, main_menu.rect)
            screen.blit(logo, (200, 50))
            player1.re_new()
            player2.re_new()
            display1.show_player()
            display2.show_player()
            display1.facing = 'right'
            display2.facing = 'left'
            if display1.counter <= 50:
                display1.last_action = "running-right"
                display1.counter += 1
                display1.run_right()
                display1.move_right(dt)
            if display2.counter <= 50:
                display2.last_action = "running-left"
                display2.counter += 1
                display2.run_left()
                display2.move_left(dt)
            if display2.counter >= 50 and display1.counter >= 50:
                screen.blit(space, (575, 400))
            game_over_count = 0

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if keys[pygame.K_SPACE]:
                game_on = True
            if keys[pygame.K_ESCAPE]:
                running = False

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
