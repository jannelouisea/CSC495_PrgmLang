from card import Card
from enums import Suit, FaceCard
from pile import Pile


class Deck(Pile):

    def __init__(self, deck_size=1, deck_w_jokers=False, deck_wo_queens=False):
        super(Deck, self).__init__()

        # Initialize list of cards
        for suit in Suit:
            # create number cards
            for n in range(2, 11):
                self.cards.append(Card(str(n), suit, n))
            # create face cards
            self.cards.append(Card(FaceCard.ACE.value, suit, 14))
            self.cards.append(Card(FaceCard.KING.value, suit, 13))
            self.cards.append(Card(FaceCard.QUEEN.value, suit, 12))
            self.cards.append(Card(FaceCard.JACK.value, suit, 11))

        # Create jokers
        if deck_w_jokers:
            self.cards.append(Card('!', '!', 0, True))
            self.cards.append(Card('!', '!', 0, True))

        for i in range(deck_size - 1):
            self.cards.insert(self.cards)

        if deck_wo_queens:
            #fix this!!!
            del(self.cards[11])
            del(self.cards[23])
            del(self.cards[35])
