import random
from thing import Thing
from card import Card
from bartokrules import BartokRules
from enums import Game

class Player(Thing):
    def __init__(self, env, index, game):
        def deterRules(game):
            if game == Game.BARTOK:
                return BartokRules()
            # Other rules from different games would go here

        self.env = env
        self.hand = list()
        self.index = index
        self.game = deterRules(game)
        self.move = None

    def sizeOfHand(self):
        return len(self.hand)

    def addToHand(self, card, faceUp=True):
        if isinstance(card, Card):
            if card.faceUp != faceUp:
                card.flip()
            self.hand.append(card)

    def removeFromHand(self, num):
        return self.hand.pop(num - 1)

    def handToStr(self):
        str = ""
        for card in self.hand:
            str = str + card.rank
        for card in self.hand:
            str = str + card.suit.value
        return str

    def removeCardFromHand(self, idx):
        return self.hand.pop(idx)

    def sortHand(self):
        pass

    def reflect(self):
        i = 1
        for card in self.hand:
            print("Card {}: {} of {}".format(i, card.rank, card.suit))
            i += 1

    def weighOptions(self):
        for rule in self.game.rules:        # Rules are sorted by highest priority
            if rule.canAct(self):           # As of right now, the strategy is to just
                self.move = rule            # act on the first rule the player can do
                print("Player", self.index + 1, "weighed", rule.name, "as the best option")
                break                       # If a player of a specific game needs more intricate
                                            # ways to weigh their options, a player subclass should
                                            # be made overwriting this method

    def act(self):
        print("Player", self.index + 1, "is playing", self.move.name)
        self.move.act(self)
