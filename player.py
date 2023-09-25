import pygame

class Player:
    def __init__(self, folder, screen, player_pos, origin, ground):
        self.folder = folder
        self.player_pos = player_pos
        self.screen = screen
        self.avatar = f'images/{self.folder}/default.png'
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
        self.is_protecting = False
        self.protect_count = 0
        self.is_knockback = False
        self.block_count = 0
        self.is_double_jump = False
        self.is_double_jump_possible = False
        self.fall_vel = 15
        self.fall_mass = -1
        #self.rect = self.image.get_rect()

        #self.rect = self.image.get_rect()


    def re_new(self, image):
        self.player_pos.x = self.origin[0]
        self.health = 100
        self.update_image(image)
        self.last_action = 'still'


    def show_player(self):
        self.image = pygame.image.load(self.avatar)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [self.player_pos.x, self.player_pos.y]
        self.screen.blit(self.image, self.rect)

    def attack(self, players):
        if self.attacking == False:
            self.last_action = "attacking"
            self.attacking = True
            for player in players:
                if player != self:
                    self.check_hitbox(player)

    def check_hitbox(self, player):
        if self.rect.colliderect(player.rect):
            if self.rect.x > player.rect.x and self.facing == 'left':
                if player.is_protecting and player.facing == 'right':
                    self.is_knockback = True
                    player.is_knockback = True
                else:
                    player.health -= self.damage
                    player.is_hit = True
            if self.rect.x < player.rect.x and self.facing == 'right':
                if player.is_protecting and player.facing == 'left':
                    self.is_knockback = True
                    player.is_knockback = True
                else:
                    player.health -= self.damage
                    player.is_hit = True

    def protect_knockback(self, player):
        if self.is_knockback:
            if self.x_vel == 0:
                self.is_knockback = False
                self.x_mass = 1
                self.x_vel = 15
                self.hit_count = 0
            else:
                self.hit_count += 1
                force_x = ((1 / 2) * self.x_mass * self.x_vel ** 2) * .15
                if 0 < self.player_pos.x < 1215:
                    if self.last_action == "attacking":
                        if self.facing == 'left':
                            self.player_pos.x += force_x
                        else:
                            self.player_pos.x -= force_x
                    else:
                        if player.facing == 'left':
                            self.player_pos.x -= force_x
                        else:
                            self.player_pos.x += force_x
                self.x_vel = self.x_vel - 1

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

    def protect(self):
        self.last_action = "protecting"
        self.is_protecting = True
        self.protect_count += 1
        if self.protect_count < 10:
            if self.facing == 'right':
                self.update_image(f"images/{self.folder}/protect/protect1.png")
            else:
                self.update_image(f"images/{self.folder}/protect/protect1rev.png")
        else:
            if self.facing == 'right':
                self.update_image(f"images/{self.folder}/protect/protect2.png")
            else:
                self.update_image(f"images/{self.folder}/protect/protect2rev.png")

    def jump(self):
        if self.is_double_jump == 0 and self.attacking == False and self.is_protecting == False:
            if self.is_double_jump_possible and self.is_jump:
                self.is_double_jump += 1
            else:
                self.last_action = "jumping"
                self.is_jump = True

    def check_on_platform(self, bg):
        on_plat = True
        is_on_main = False
        for ground in bg.ground_objects:
            if ground.is_main_ground:
                if self.rect.x + self.rect.width < ground.rect:
                    if ground.is_main_ground:
                        is_on_main = True
        return on_plat

    def gravity(self, bg):
        if not self.is_jump:
            if not self.check_on_platform(bg):
                print('should fall')



    def move_left(self, dt):
        if self.is_protecting == False or self.is_jump:
            self.last_action = "running-left"
            self.facing = 'left'
            if self.player_pos.x > 0:
                self.player_pos.x -= 400 * dt
            self.run_left()

    def move_right(self, dt):
        if self.is_protecting == False or self.is_jump:
            self.last_action = "running-right"
            self.facing = 'right'
            if self.player_pos.x < 1215:
                self.player_pos.x += 400 * dt
            self.run_right()

    def special_attack(self):
        print(f'{self.name} doing special attack')

    def update_image(self, image):
        self.avatar = image

    def run_right(self):
        if self.last_action == "running-right" and self.is_jump == False and self.is_hit == False:
            self.counter += 1
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
            self.counter += 1
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
        elif -9 <= self.vel <= -2:
            if self.facing == 'right':
                self.update_image(f"images/{self.folder}/jumpAnimation/jump5.png")
            else:
                self.update_image(f"images/{self.folder}/jumpAnimation/jump5rev.png")
        elif -14 <= self.vel <= -9:
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

    def check_player_jump(self, bg):
        jump_stop = False
        if self.is_jump and self.is_hit == False:
            if self.is_double_jump == 1:
                self.is_double_jump += 1
                self.mass = 1
                self.vel = 15
                self.jump_count = 0
            for ground in bg.ground_objects:
                if pygame.Rect.colliderect(self.rect, ground.rect) and self.jump_count != 0 and self.vel < 0:
                    if self.player_pos.y + self.rect.height <= ground.rect.y + ground.rect.height:
                        self.player_pos.y = ground.rect.y - self.rect.height
                        self.is_jump = False
                        self.is_double_jump = 0
                        self.is_double_jump_possible = False
                        self.mass = 1
                        self.vel = 15
                        self.jump_count = 0
                        jump_stop = True
            if not jump_stop:
                self.jump_count += 1
                if self.vel < 0:
                    self.mass = -1
                force = ((1 / 2) * self.mass * self.vel ** 2) * .2
                self.player_pos.y -= force
                self.vel = self.vel - .5
        self.do_jump_animation()

    def update_to_idle(self):
        if ((self.last_action == "still" or self.last_action == "jumping") and not self.is_jump) or (self.last_action == "protecting" and not self.is_protecting):
            if self.facing == 'left':
                self.update_image(f"images/{self.folder}/reverse.png")
            else:
                self.update_image(f"images/{self.folder}/default.png")

    def is_doing_nothing(self):
        if self.is_protecting == False and self.is_jump == False and self.attacking == False:
            return True
        else:
            return False

