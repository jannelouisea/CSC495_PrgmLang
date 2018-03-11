from game import Game
from deck import Deck
from player import Player
from pile import Pile

class Bartok(Game):
    def __init__(self):
        super(Bartok, self).__init__()
        self.env['center'] = Pile()

    def setUp(self):
        print("Setting up Bartok")
        self.env['deck'] = Deck()       # Deck without Jokers
        self.env['deck'].shuffle()

        # These numbers ensure that there are always cards left in the deck when the
        # game starts.

        numOfPlayers = int(input("How many players? Number must be between 2 and 5.\n> "))
        if numOfPlayers < 2 or numOfPlayers > 5:
            self.cancel("Incorrect numbers of players. Canceling game.")

        numStartCards = int(input("How many cards should each player start with? Must be between 5 or 7 cards.\n> "))
        if numStartCards < 5 or numStartCards > 7:
            self.cancel("Invalid number of starting cards. Canceling game.")

        for i in range(numOfPlayers):
            player = Player(self.env)
            for i in range(numStartCards):
                player.addToHand(self.env['deck'].take())
            self.env['players'].append(player)

        # Add top card in deck onto center pile
        self.env['center'].put(self.env['deck'].take())

    def play(self):
        print("Let's play Bartok!")
