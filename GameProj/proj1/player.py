from thing import Thing
from card import Card

class Player(Thing):
    def __init__(self, env):
        self.env = env
        self.hand = list()

    def addToHand(self, card, faceUp):
        if isinstance(card, Card):
            if card.faceUp != faceUp:
                card.flip()
            self.hand.append(card)

    def reflect(self):
        pass

    def act(self):
        pass
