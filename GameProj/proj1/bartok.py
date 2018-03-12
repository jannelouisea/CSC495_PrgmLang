from game import Game
from deck import Deck
from player import Player
from pile import Pile

class Bartok(Game):
    def __init__(self, game):
        super(Bartok, self).__init__(game)
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
        self.env['numOfPlayers'] = numOfPlayers

        numStartCards = int(input("How many cards should each player start with? Must be between 5 or 7 cards.\n> "))
        if numStartCards < 5 or numStartCards > 7:
            self.cancel("Invalid number of starting cards. Canceling game.")

        for i in range(numOfPlayers):
            player = Player(self.env, i, self.game)
            for i in range(numStartCards):
                player.addToHand(self.env['deck'].takeTop())
            self.env['players'].append(player)

        # Add top card in deck onto center pile
        self.env['center'].put(self.env['deck'].takeTop())

    def play(self):
        print("Let's play Bartok!")
        while(self.env['winner'] < 0):
            topCard = self.env['center'].checkTopCard()
            print("Center Card: ({} {})".format(topCard.rank, topCard.suit))
            currPlayer = self.env['players'][self.env['currPlayer']]
            currPlayer.weighOptions()
            currPlayer.act()
            self.detWinner()
        print("Player {} has won the game!".format(self.env['winner']))

    def detWinner(self):
        for player in self.env['players']:
            if player.sizeOfHand() == 0:
                self.env['winner'] = player.index
