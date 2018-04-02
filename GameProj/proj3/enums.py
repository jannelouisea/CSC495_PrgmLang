from enum import Enum


class Suit(Enum):
    SPADES = 'S'
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'


class FaceCard(Enum):
    KING = 'K'
    QUEEN = 'Q'
    JACK = 'J'
    ACE = 'A'


class Color(Enum):
    BLACK = 0
    RED = 1


class Direction(Enum):
    CLOCKWISE = 1
    CRCLOCKWISE = -1


class Game(Enum):
    BARTOK = 0,
    SPOONS = 1


class BartokRuleEnum(Enum):
    PLACEDRAW2 = 0
    DRAW2 = 1
    PLACECARD = 2
    DRAWCARD = 3


# TODO: Take out?
class PileActions(Enum):
    TAKE = 0,
    TAKETOP = 1,
    TAKEBOTTOM = 2,
    LOOK = 3,
    LOOKTOP = 4,
    LOOKBOTTOM = 5,
    PUT = 6
