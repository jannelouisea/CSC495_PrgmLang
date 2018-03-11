from thing import Thing
from card import Card

class Player(Thing):
    def __init__(self, env):
        self.env = env
        self.hand = list()

    def addToHand(self, card, faceUp=True):
        if isinstance(card, Card):
            if card.faceUp != faceUp:
                card.flip()
            self.hand.append(card)

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
        pass

    def act(self):
        pass
