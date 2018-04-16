from card import Card
from random import shuffle
import copy
from thing import Thing

# Pile class manages a stack of cards
class Pile(Thing):
    def __init__(self):
        self.cards = list()     # implemented as a stack

    def is_empty(self):
        return len(self.cards) < 1

    def num_cards(self):
        return len(self.cards)

    def look(self, index):
        return copy.deepcopy(self.cards[index])

    def look_top(self):
        return self.look(-1)

    def look_bottom(self):
        return self.look(0)

    def take(self, idx=None):
        if idx:
            return self.cards.pop(idx)
        else:
            return self.cards.pop()

    # Removes and then returns the top card
    def take_top(self):
        return self.take()

    def take_bottom(self):
        return self.take(0)

    # Adds a new card onto the stack of cards
    def put(self, card, face_up=True):
        if isinstance(card, Card):
            if card.face_up != face_up:
                card.flip()
            self.cards.append(card)

    # Shuffles deck of cards
    def shuffle(self):
        shuffle(self.cards)

    def sort_cards(self, sort_func):
        self.cards = sort_func(self.cards)
