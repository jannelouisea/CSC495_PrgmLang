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
            player = Player(self.env, i, self.game)
            for i in range(self.initHandCount):
                player.addToHand(self.env['deck'].takeTop())
            self.env['players'].append(player)

        # Init end player, player who only contributes to the trash pile
        self.env['endPlayer'] = numOfPlayers - 1

    def fourOfAKind(self, player):
        pattern = re.compile(r"(2){4}|(3){4}|(4){4}|(5){4}|(6){4}|(7){4}|(8){4}|(9){4}|(J){4}|(Q){4}|(K){4}|(A){4}(S|H|D|C){4}")
        print player.handToStr();
        if pattern.match(player.handToStr()):
            self.env['winner'] = player.index
            return True
        return False


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
                    print("Player {} these are your cards: ".format(i))
                    #adds card from hand to trash pile
                    player.reflect()
                    num = int(input("Please input the card number to discard (1-5) \n"))
                    if num < 1 & num > 5:
                        num = int(input("Please input a number between 1 and 5 \n"))
                    self.env['trash'].put(player.hand.pop(num - 1))
                elif i == 0:
                    #adds new card from deck
                    if len(self.env['deck'].cards) == 0:
                        #shuffle these???
                        self.env['deck'] = self.env['trash']
                    player.addToHand(self.env['deck'].takeTop())
                    print("Player 0 these are your cards: ")
                    player.reflect()
                    num = int(input("Please input the card number to discard (1-5) \n"))
                    if num < 1 & num > 5:
                        num = int(input("Please input a number between 1 and 5 \n"))
                    #gives card to next player
                    temp.append(player.hand.pop(num-1))
                else:
                    #adds card that player gave
                    player.addToHand(temp.pop())
                    print("Player {} these are your cards: ".format(i))
                    #gives card to next player
                    player.reflect()
                    num = int(input("Please input the card number to discard (1-5) \n"))
                    if num < 1 & num > 5:
                        num = int(input("Please input a number between 1 and 5 \n"))
                    temp.append(player.hand.pop(num-1))
        print("Player {} these are your cards: ".format(i))
        player.reflect()
        print('Player {} has won'.format(i))

