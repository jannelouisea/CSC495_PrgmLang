from card import Card
from enums import Suit, FaceCard
from pile import Pile


class Deck(Pile):

    def __init__(self, jokers_included=False):
        super(Deck, self).__init__()

        # Initialize list of cards
        for suit in Suit:
            # create number cards
            for n in range(2, 10):
                self.cards.append(Card(str(n), suit, n))
            # create face cards
            self.cards.append(Card(FaceCard.ACE.value, suit, 13))
            self.cards.append(Card(FaceCard.KING.value, suit, 12))
            self.cards.append(Card(FaceCard.QUEEN.value, suit, 11))
            self.cards.append(Card(FaceCard.JACK.value, suit, 10))

        # Create jokers
        if jokers_included:
            self.cards.append(Card('!', '!', 0, True))
            self.cards.append(Card('!', '!', 0, True))
