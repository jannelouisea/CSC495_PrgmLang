from enums import FaceCard, Suit, Color


class Card():

    def __init__(self, rank, suit, value, face_up=True, joker=False):     # constructor
        self.rank = rank                    # {2,3,...,King,Ace} Jokers are not included
        self.suit = suit                    # Must be an enum of Suit
        self.value = value                  # point value of the card
        self.color = self.det_color()
        self.joker = joker                  # boolean value
        self.face_up = face_up              # boolean value
        self.suitImg = self.det_suit_img()

    def det_color(self):
        if self.suit == Suit.CLUBS or self.suit == Suit.SPADES:
            return Color.BLACK
        else:
            return Color.RED

    def det_suit_img(self):
        if self.suit == Suit.SPADES:
            return "\u2660"
        elif self.suit == Suit.DIAMONDS:
            return "\u2666"
        elif self.suit == Suit.CLUBS:
            return "\u2663"
        elif self.suit == Suit.HEARTS:
            return "\u2665"

    def get_info(self):
        return self.rank, self.suit, self.value, self.joker, self.color

    def is_face_card(self):
        return self.rank in FaceCard.__members__

    def flip(self):
        self.face_up = not self.face_up

    def matches_rank(self, rank):
        return self.rank == rank

    def matches_suit(self, suit):
        return self.suit == suit

    def matches_card(self, card):
        return self.rank == card.rank and self.suit == card.suit

    def __str__(self):
        return f'[{self.rank} {self.suitImg}]'

    def __repr__(self):
        return f'[{self.rank} {self.suitImg}]'
