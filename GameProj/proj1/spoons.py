from game import Game
from deck import Deck
from player import Player
from pile import Pile

class Spoons(Game):

    def __init__(self):
        super(Spoons, self).__init__()
        self.initHandCount = 4
        self.env['trash'] = Pile()

    def setUp(self):
        print("Setting up Spoons...")
        self.env['deck'] = Deck()       # Deck without Jokers
        self.env['deck'].shuffle()

        # Init players
        numOfPlayers = int(input("How many players? Number must be between 3 and 13.\n> "))
        if numOfPlayers < 3 or numOfPlayers > 13:
            self.cancel("Incorrect numbers of players. Canceling game.")

        # Init each player's hand
        for i in range(numOfPlayers):
            player = Player(self.env)
            for i in range(self.initHandCount):
                player.addToHand(self.env['deck'].take())
            self.env['players'].append(player)


    def play(self):
        print("Let's play Spoons!")
