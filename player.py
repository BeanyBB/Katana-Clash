import pygame

class Player:
    def __init__(self, weapon, avatar, name, screen, player_pos, color):
        self.color = color
        self.player_pos = player_pos
        self.screen = screen
        self.weapon = weapon
        self.avatar = avatar
        self.name = name
        self.last_action = 'still'
        self.counter = 0
        self.is_jump = False
        self.mass = 1
        self.vel = 15
        self.jump_count = 0
        self.facing = 'right'

    def show_player(self):
        self.image = pygame.image.load(self.avatar)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [self.player_pos.x, self.player_pos.y]
        self.screen.blit(self.image, self.rect)

    def attack(self):
        print(f'{self.name} attacking')

    def defend(self):
        print(f'{self.name} defending')

    def jump(self):
        if self.is_jump == False:
            self.is_jump = True

    def move_left(self, dt):
        self.facing = 'left'
        self.player_pos.x -= 400 * dt

    def move_right(self, dt):
        self.facing = 'right'
        self.player_pos.x += 400 * dt

    def special_attack(self):
        print(f'{self.name} doing special attack')

    def update_image(self, image):
        self.avatar = image

    def run_right(self):
        if self.last_action == "running-right" and self.is_jump == False:
            if 0 < self.counter < 7.5:
                self.update_image("images/runAnimation/run1.png")
            elif 7.5 <= self.counter < 15:
                self.update_image("images/runAnimation/run2.png")
            elif 15 <= self.counter < 22.5:
                self.update_image("images/runAnimation/run3.png")
            elif 22.5 <= self.counter < 30:
                self.update_image("images/runAnimation/run4.png")
            elif 30 <= self.counter < 37.5:
                self.update_image("images/runAnimation/run5.png")
            elif 37.5 <= self.counter < 45:
                self.update_image("images/runAnimation/run6.png")
            elif 45 <= self.counter < 52.5:
                self.update_image("images/runAnimation/run7.png")
            else:
                self.update_image("images/runAnimation/run8.png")
                self.counter = 0
        else:
            self.counter = 0

    def run_left(self):
        if self.last_action == "running-left" and self.is_jump == False:
            if 0 < self.counter < 7.5:
                self.update_image("images/runAnimation/run1rev.png")
            elif 7.5 <= self.counter < 15:
                self.update_image("images/runAnimation/run2rev.png")
            elif 15 <= self.counter < 22.5:
                self.update_image("images/runAnimation/run3rev.png")
            elif 22.5 <= self.counter < 30:
                self.update_image("images/runAnimation/run4rev.png")
            elif 30 <= self.counter < 37.5:
                self.update_image("images/runAnimation/run5rev.png")
            elif 37.5 <= self.counter < 45:
                self.update_image("images/runAnimation/run6rev.png")
            elif 45 <= self.counter < 52.5:
                self.update_image("images/runAnimation/run7rev.png")
            else:
                self.update_image("images/runAnimation/run8rev.png")
                self.counter = 0
        else:
            self.counter = 0
