
class Player:
    def __init__(self, weapon, avatar, name):
        self.weapon = weapon
        self.avatar = avatar
        self.name = name

    def attack(self):
        print(f'{self.name} attacking')

    def defend(self):
        print(f'{self.name} defending')

    def jump(self):
        print(f'{self.name} jumping')

    def move_left(self):
        print(f'{self.name} moving left')

    def move_right(self):
        print(f'{self.name} moving right')

    def special_attack(self):
        print(f'{self.name} doing special attack')