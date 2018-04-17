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
    PLAYDRAW2 = 'Play Draw2 Card (rank 2)'
    DRAW2 = 'Draw 2n Cards (n = draw2 effect)'
    PLAYSKIP = 'Play Skip Card (rank 7)'
    PLAYREVERSE = 'Play Reverse Card (rank 8)'
    PLAYMATCHCARD = 'Play Card w/ Matching Suit or Rank'
    DRAWCARD = 'Draw from Deck'


class SevensRuleEnum(Enum):
    PLAYSTARTCARD = 'Play Start Card (7 Diamonds)'
    PLAYSTARTLAYOUTCARD = 'Play Start Layout Card (rank 7)'
    PLAYADJACENTCARD = 'Play Adjacent Card'
    KNOCK = 'Knock (can\'t play any cards)'


class SpoonsRuleEnum(Enum):
    DEALER = 'Draw card from deck'
    PASS = 'Discard card to next player'
    END = 'Discard card to trash pile'
