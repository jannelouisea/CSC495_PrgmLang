from enums import FaceCard
from thing import Thing

class Card(Thing):

    def __init__(self, rank, suit, value, joker=False):     # constructor
        self.rank = rank            # {2,3,...,King,Ace} Jokers are not included
        self.suit = suit            # Must be an enum of FaceCard
        self.value = value          # point value of the card
        self.joker = joker          # boolean value
        self.face_up = False        # boolean value

    def isFaceCard(self):
        return self.rank in FaceCard.__members__

    def flip(self):
        self.face_up = not(self.face_up)
