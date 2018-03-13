from card import Card
from thing import Thing
from random import shuffle
import copy

# Pile class manages a stack of cards
class Pile(Thing):
    def __init__(self):
        self.cards = list()     # implemented as a stack

    def isEmpty(self):
        return (len(self.cards) < 1)

    def numOfCards(self):
        return len(self.cards)

    # Returns a tuple of information about the top card
    def checkTopCard(self):
        # return self.cards[-1].getInfo()
        return copy.deepcopy(self.cards[-1])

    # Removes and then returns the top card
    def takeTop(self):
        return self.cards.pop()

    def takeBottom(self):
        return self.cards.pop(0)

    # Adds a new card onto the stack of cards
    def put(self, card, faceUp=True):
        if isinstance(card, Card):
            if card.faceUp != faceUp:
                card.flip()
            self.cards.append(card)

    # Shuffles deck of cards
    def shuffle(self):
        shuffle(self.cards)