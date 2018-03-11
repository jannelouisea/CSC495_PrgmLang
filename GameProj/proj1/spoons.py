from game import Game
from deck import Deck
from player import Player

class Spoons(Game):

    def __init__(self):
        super(Spoons, self).__init__()
        self.initHandCount = 4

    def setUp(self):
        print("Setting up Spoons...")
        self.env['deck'] = Deck()       # Deck without Jokers
        self.env['deck'].shuffle()

        numOfPlayers = int(input("How many players? Number must be between 3 and 13.\n> "))
        if numOfPlayers < 3 or numOfPlayers > 13:
            self.cancel("Incorrect numbers of players. Canceling game.")

        for i in range(numOfPlayers):
            player = Player(self.env)
            for i in range(self.initHandCount):
                player.addToHand(self.env['deck'].take())

            self.env['players'].append(player)

        for player in self.env['players']:
            print(player.handToStr())

    def play(self):
        print("Let's play Spoons!")
