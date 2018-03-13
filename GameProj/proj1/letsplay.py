import sys
from spoons import Spoons
from bartok import Bartok
from enums import Game
# from deck import Deck

# deck_no_jokers = Deck()       # Creates a standard 52 deck WITHOUT jokers
# deck_w_jokers = Deck(True)       # Creates a standard 52 deck WITHOUT jokers

if __name__ == '__main__':
    # print(deck_no_jokers.__repr__())
    # print('===================')
    # print(deck_w_jokers.__repr__())
    print("Let's Play! :D")
    gameChoice = int(input("Which game would you like to play?\n0 - Bartok\n1 - Spoons\n> "))
    game = None
    if gameChoice == 0:
        print ("You chose Bartok!")
        game =  Bartok(Game.BARTOK)
    elif gameChoice == 1:
        print ("You chose Spoons!")
        game = Spoons(Game.SPOONS)
    else:
        sys.exit("Incorrect value submitted. Canceling game.")

    game.setUp()
    game.play()


