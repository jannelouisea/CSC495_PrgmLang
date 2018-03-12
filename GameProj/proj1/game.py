from thing import Thing
from enums import Direction
import sys

class Game(Thing):
    def __init__(self):
        self.env = {
            'players': list(),                      # list of Players
            'currPlayer': 0,                        # index of current player
            'startPlayer': 0,                       # index of player who starts the game
            'endPlayer' : 0,                        # index of player who ends the game
            'direction': Direction.CLOCKWISE,       # Clockwise
            'deck': None,                           # Deck of cards
            'winner': -1                            # index of player who won the game, -1 for no winner
        }

    def deal(self, numOfCards): pass

    def play(self): pass

    def setUp(self): pass

    def cancel(self, msg): sys.exit(msg)
