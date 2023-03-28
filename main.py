from player import Player

def main():
    player1 = Player('sword', 'default', 'player1')
    player2 = Player('sword', 'default', 'player2')
    player1.attack()
    player2.attack()
    player2.defend()
    player2.defend()
    player1.special_attack()


if __name__ == '__main__':
    main()


