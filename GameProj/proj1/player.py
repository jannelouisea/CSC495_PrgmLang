import random
from thing import Thing
from card import Card

class Player(Thing):
    def __init__(self, env, index):
        self.env = env
        self.hand = list()
        self.index = index

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

    def sortHand(self):
        pass

    def reflect(self):
        i = 1
        for card in self.hand:
            print "Card {}: {} of {}".format(i, card.rank, card.suit)
            i += 1

    def act(self):
        pass
