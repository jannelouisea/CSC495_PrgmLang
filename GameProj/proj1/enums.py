from enum import Enum

class Suit(Enum):
    SPADES = 'S',
    HEARTS = 'H',
    DIAMONDS = 'D',
    CLUBS = 'C'

class FaceCard(Enum):
    KING = 'K',
    QUEEN = 'Q',
    JACK = 'J',
    ACE = 'A'

class Color(Enum):
    BLACK = 0,
    RED = 1

class Direction(Enum):
    CLOCKWISE = 1,
    CRCLOCKWISE = -1
