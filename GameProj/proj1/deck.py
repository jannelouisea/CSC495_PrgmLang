from card import Card
from enums import Suit, FaceCard
from thing import Thing

class Deck(Thing):

    def __init__(self, jokers_included=False):
        # Declare list of cards
        self.deck = list()

        # Initialize list of cards
        for suit in Suit.__members__:
            # create number cards
            for n in range(2,10):
                self.deck.append(Card(str(n), suit, n))
            # create face cards
            self.deck.append(Card(FaceCard.ACE, suit, 13))
            self.deck.append(Card(FaceCard.KING, suit, 12))
            self.deck.append(Card(FaceCard.QUEEN, suit, 11))
            self.deck.append(Card(FaceCard.JACK, suit, 10))

        # Create jokers
        if (jokers_included):
            self.deck.append(Card('Z', 'Z', 0, True))
            self.deck.append(Card('Z', 'Z', 0, True))
