from game import Game
from deck import Deck
from player import Player
from pile import Pile

class Bartok(Game):
    def __init__(self, game):
        super(Bartok, self).__init__(game)
        self.env['center'] = Pile()
        # Determines if the current player mustDraw2
        self.env['mustDraw2'] = False
        # Keeps track of the number of players who cumulatively Draw 2
        self.env['draw2Effect'] = 0

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
        print('''
Bartok Requirements:
 A standard deck of cards (without Jokers)
 2 to 5 players
 5 to 7 card to start
Game Play:
 The first player to get rid of all cards from their hand wins.
 Each player is initially dealt five to seven cards.
 Players place cards in the center Pile.
 After dealing cards to each player, the top card from the deck is placed
 face up in the center.
 Each player must place a card matching the suit or rank of the 
 top card of the center pile.
 If a player cannot place a card, they must draw one card from the deck (This is done automatically).
 If the top card is a Draw 2 card (i.e. card with rank 2) and the player cannot
 add another Draw 2 card, they must draw n cards from the deck where n equals the number
 of cumulative Draw 2 cards * 2 (This is also done automatically).
        ''')


        while (self.env['winner'] < 0):
            topCard = self.env['center'].checkTopCard()
            print("=============================")
            print("Center Card: ({} {})".format(topCard.rank, topCard.suit))
            print("=============================")
            currPlayer = self.env['players'][self.env['currPlayer']]
            print(f"Player {currPlayer.index + 1} turn")
            print("-----------------------------")
            currPlayer.weighOptions()
            currPlayer.act()
            self.detWinner()
        print("Player {} has won the game!".format(self.env['winner']))

    def detWinner(self):
        for player in self.env['players']:
            if player.sizeOfHand() == 0:
                self.env['winner'] = player.index
