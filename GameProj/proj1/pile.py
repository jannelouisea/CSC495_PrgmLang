from card import Card
from thing import Thing

# Pile class manages a stack of cards
class Pile(Thing):
    def __init__(self):
        self.cards = list()     # implemented as a stack

    # Returns a tuple of information about the top card
    def checkTopCard(self):
        return self.cards[-1].getInfo()

    # Removes and then returns the top card
    def take(self):
        return self.cards.pop()

    # Adds a new card onto the stack of cards
    def put(self, card, faceUp=True):
        if isinstance(card, Card):
            if card.faceUp != faceUp:
                card.flip()
            self.cards.append(card)
