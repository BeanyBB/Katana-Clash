import pygame

class Player:
    def __init__(self, weapon, avatar, name, screen, player_pos, color):
        self.color = color
        self.player_pos = player_pos
        self.screen = screen
        self.weapon = weapon
        self.avatar = avatar
        self.name = name

    def show_player(self):
        pygame.draw.circle(self.screen, self.color, self.player_pos, 40)

    def attack(self):
        print(f'{self.name} attacking')

    def defend(self):
        print(f'{self.name} defending')

    def jump(self):
        print(f'{self.name} jumping')

    def move_left(self, dt):
        self.player_pos.x -= 300 * dt
        print(f'{self.name} moving left')

    def move_right(self, dt):
        print(self.player_pos)
        self.player_pos.x += 300 * dt
        print(f'{self.name} moving right')
        print(self.player_pos)

    def special_attack(self):
        print(f'{self.name} doing special attack')