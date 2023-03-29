import pygame

class Player:
    def __init__(self, weapon, folder, name, screen, player_pos, color, origin):
        self.color = color
        self.folder = folder
        self.player_pos = player_pos
        self.screen = screen
        self.weapon = weapon
        self.avatar = f'images/{self.folder}/default.png'
        self.name = name
        self.last_action = 'still'
        self.counter = 0
        self.is_jump = False
        self.mass = 1
        self.vel = 15
        self.jump_count = 0
        self.facing = 'right'
        self.attacking = False
        self.attack_count = 0
        self.health = 100
        self.damage = 10
        self.origin = origin
        self.is_hit = False
        self.hit_count = 0
        self.x_mass = 1
        self.x_vel = 15

    def show_player(self):
        self.image = pygame.image.load(self.avatar)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [self.player_pos.x, self.player_pos.y]
        self.screen.blit(self.image, self.rect)

    def attack(self, player):
        if self.attacking == False:
            self.attacking = True
            self.check_hitbox(player)

    def check_hitbox(self, player):
        if self.rect.colliderect(player.rect):
            if self.rect.x > player.rect.x and self.facing == 'left':
                player.health -= self.damage
                player.get_hit()
            if self.rect.x < player.rect.x and self.facing == 'right':
                player.health -= self.damage
                player.get_hit()
    def get_hit(self):
        self.is_hit = True

    def check_player_hit(self, attacker):
        if self.is_hit:
            if self.x_vel == 0:
                self.is_hit = False
                self.x_mass = 1
                self.x_vel = 15
                self.hit_count = 0
            else:
                self.hit_count += 1
                force_x = ((1 / 2) * self.x_mass * self.x_vel ** 2) * .7
                if 0 < self.player_pos.x < 1215:
                    if attacker.facing == 'left':
                        self.player_pos.x -= force_x
                    else:
                        self.player_pos.x += force_x
                self.x_vel = self.x_vel - 1

    def defend(self):
        print(f'{self.name} defending')

    def jump(self):
        if self.is_jump == False and self.attacking == False:
            self.is_jump = True

    def move_left(self, dt):
        self.facing = 'left'
        if self.player_pos.x > 0:
            self.player_pos.x -= 400 * dt

    def move_right(self, dt):
        self.facing = 'right'
        if self.player_pos.x < 1215:
            self.player_pos.x += 400 * dt

    def special_attack(self):
        print(f'{self.name} doing special attack')

    def update_image(self, image):
        self.avatar = image

    def run_right(self):
        if self.last_action == "running-right" and self.is_jump == False and self.is_hit == False:
            if 0 < self.counter < 7.5:
                self.update_image(f"images/{self.folder}/runAnimation/run1.png")
            elif 7.5 <= self.counter < 15:
                self.update_image(f"images/{self.folder}/runAnimation/run2.png")
            elif 15 <= self.counter < 22.5:
                self.update_image(f"images/{self.folder}/runAnimation/run3.png")
            elif 22.5 <= self.counter < 30:
                self.update_image(f"images/{self.folder}/runAnimation/run4.png")
            elif 30 <= self.counter < 37.5:
                self.update_image(f"images/{self.folder}/runAnimation/run5.png")
            elif 37.5 <= self.counter < 45:
                self.update_image(f"images/{self.folder}/runAnimation/run6.png")
            elif 45 <= self.counter < 52.5:
                self.update_image(f"images/{self.folder}/runAnimation/run7.png")
            else:
                self.update_image(f"images/{self.folder}/runAnimation/run8.png")
                self.counter = 0
        else:
            self.counter = 0

    def run_left(self):
        if self.last_action == "running-left" and self.is_jump == False and self.is_hit == False:
            if 0 < self.counter < 7.5:
                self.update_image(f"images/{self.folder}/runAnimation/run1rev.png")
            elif 7.5 <= self.counter < 15:
                self.update_image(f"images/{self.folder}/runAnimation/run2rev.png")
            elif 15 <= self.counter < 22.5:
                self.update_image(f"images/{self.folder}/runAnimation/run3rev.png")
            elif 22.5 <= self.counter < 30:
                self.update_image(f"images/{self.folder}/runAnimation/run4rev.png")
            elif 30 <= self.counter < 37.5:
                self.update_image(f"images/{self.folder}/runAnimation/run5rev.png")
            elif 37.5 <= self.counter < 45:
                self.update_image(f"images/{self.folder}/runAnimation/run6rev.png")
            elif 45 <= self.counter < 52.5:
                self.update_image(f"images/{self.folder}/runAnimation/run7rev.png")
            else:
                self.update_image(f"images/{self.folder}/runAnimation/run8rev.png")
                self.counter = 0
        else:
            self.counter = 0

    def do_jump_animation(self):
        #if self.attacking == False:
            if 13 <= self.vel <= 15:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump1.png")
                else:
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump1rev.png")
            elif 11 <= self.vel <= 13:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump2.png")
                else:
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump2rev.png")
            elif 0 <= self.vel <= 11:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump4.png")
                else:
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump3rev.png")
            elif -2 <= self.vel <= 0:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump4.png")
                else:
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump4rev.png")
            elif -12 <= self.vel <= -2:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump5.png")
                else:
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump5rev.png")
            elif -14 <= self.vel <= -12:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump6.png")
                else:
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump6rev.png")
            else:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump7.png")
                else:
                    self.update_image(f"images/{self.folder}/jumpAnimation/jump7rev.png")

    def check_player_attack(self):
        if self.attacking and self.is_hit == False:
            self.attack_count += 1
            if self.attack_count < 15:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/attack/attack1.png")
                else:
                    self.update_image(f"images/{self.folder}/attack/attack1rev.png")
            elif self.attack_count <= 30:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/attack/attack2.png")
                else:
                    self.update_image(f"images/{self.folder}/attack/attack2rev.png")
            elif self.attack_count <= 45:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/attack/attack3.png")
                else:
                    self.update_image(f"images/{self.folder}/attack/attack3rev.png")
            else:
                if self.facing == 'right':
                    self.update_image(f"images/{self.folder}/default.png")
                else:
                    self.update_image(f"images/{self.folder}/reverse.png")
                self.attacking = False
                self.attack_count = 0

    def check_player_jump(self):
        if self.is_jump and self.is_hit == False:
            if self.player_pos.y == self.origin and self.jump_count != 0:
                self.is_jump = False
                self.mass = 1
                self.vel = 15
                self.jump_count = 0
            else:
                self.jump_count += 1
                if self.vel < 0:
                    self.mass = -1
                force = ((1 / 2) * self.mass * self.vel ** 2) * .4
                self.player_pos.y -= force
                self.vel = self.vel - .5
            self.do_jump_animation()
