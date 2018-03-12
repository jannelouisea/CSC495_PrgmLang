import re
from game import Game
from deck import Deck
from player import Player
from pile import Pile
from enums import Suit

class Spoons(Game):

    def __init__(self, game):
        super(Spoons, self).__init__(game)
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
            player = Player(self.env, i)
            for i in range(self.initHandCount):
                player.addToHand(self.env['deck'].take())
            self.env['players'].append(player)

        # Init end player, player who only contributes to the trash pile
        self.env['endPlayer'] = numOfPlayers - 1

        # return self.env     # You don't need to return self.env it is a variable accessible to all objects

    def fourOfAKind(self, player):
        # canAct()
        pattern = re.compile("(2|3|4|5|6|7|8|9|J|Q|K){4}SHDC")
        if pattern.match(player.handToStr()):
            self.env['winner'] = player.index
            return True
        return False

    def suitCheck(self, suit):
        if suit == "Spades":
            return Suit.SPADES
        elif suit == "Clubs":
            return Suit.CLUBS
        elif suit == "Diamonds":
            return Suit.DIAMONDS
        elif suit == "Hearts":
            return Suit.HEARTS
        else:
            return "Invalid suit"


    def play(self):
        print("Let's play Spoons!")
        numOfPlayers = len(self.env['players'])
        temp = []  # should always have only one card
        player = self.env['players'][0]
        while Spoons.fourOfAKind(self, player) == False:
            for i in range(numOfPlayers):
                if Spoons.fourOfAKind(self, player) == True:
                    break
                player = self.env['players'][i]
                if i == numOfPlayers - 1:
                    #adds card that player gave
                    player.addToHand(temp.pop())
                    #adds card from hand to trash pile
                    self.env['trash'].put(player.removeFromHand())
                elif i == 0:
                    #adds new card from deck
                    if len(self.env['deck'].cards) == 0:
                        #shuffle these???
                        self.env['deck'] = self.env['trash']
                    player.addToHand(self.env['deck'].take())
                    print("Player 0 these are your cards: ")
                    player.reflect()
                    num = int(input("Please input the card number to discard (1-5) \n"))
                    #gives card to next player
                    
                    #TODO: remove the specified card
                    temp.append(player.removeFromHand(self, num))
                else:
                    #adds card that player gave
                    player.addToHand(temp.pop())
                    #gives card to next player
                    temp.append(player.removeFromHand())
        print('Player {} has won'.format(i))

