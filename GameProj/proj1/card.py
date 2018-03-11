from enums import FaceCard, Suit, Color
from thing import Thing

class Card(Thing):

    def __init__(self, rank, suit, value, joker=False):     # constructor
        self.rank = rank            # {2,3,...,King,Ace} Jokers are not included
        self.suit = suit            # Must be an enum of Suit
        self.value = value          # point value of the card
        self.color = self.detColor()
        self.joker = joker          # boolean value
        self.faceUp = False        # boolean value

    def detColor(self):
        if self.suit == Suit.CLUBS or self.suit == Suit.SPADES:
            return Color.BLACK
        else:
            return Color.RED

    def getInfo(self):
        return self.rank, self.suit, self.value, self.joker, self.color

    def isFaceCard(self):
        return self.rank in FaceCard.__members__

    def flip(self):
        self.faceUp = not(self.faceUp)

    def equalsRank(self, card):
        if isinstance(card, Card):
            return card.rank == self.rank
        else:
            return False

    def equalsSuit(self, card):
        if isinstance(card, Card):
            return card.suit == self.suit
        else:
            return False

