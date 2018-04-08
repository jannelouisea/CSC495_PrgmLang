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


class Game(Enum):
    BARTOK = 'Bartok'
    SPOONS = 'Spoons'
    SEVENS = 'Sevens'


class BartokRuleEnum(Enum):
    PLACEDRAW2 = 'Play Draw 2 Card (rank 2)'
    DRAW2 = 'Draw 2n Cards (n = draw2 effect)'
    SKIP = 'Play Skip Card (rank 7)'
    REVERSE = 'Play Reverse Card (rank 8)'
    PLACEMATCHCARD = 'Play Card w/ Matching Suit or Rank'
    DRAWCARD = 'Draw From Deck'


class SevensRuleEnum(Enum):
    PLAYSTARTCARD = 'Play Start Card (7 Diamonds)'
    PLAYSTARTLAYOUTCARD = 'Play Start Layout Card (rank 7)'
    PLAYADJACENTCARD = 'Play Adjacent Card'
    KNOCK = 'Knock (can\'t play any cards)'
