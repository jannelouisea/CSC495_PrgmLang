from game import Game
from deck import Deck

class Spoons(Game):
    def setUp(self):
        print("Setting up Spoons...")
        self.env['deck'] = Deck()       # Deck without Jokers
        self.env['deck'].shuffle()
        numOfPlayers = int(input("How many players?\n> "))



    def play(self):
        print("Let's play Spoons!")
