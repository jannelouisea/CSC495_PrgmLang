from card import Card
from enums import Suit, FaceCard
from thing import Thing
from random import shuffle
from pile import Pile

class Deck(Pile):

    def __init__(self, jokers_included=False):
        super(Deck, self).__init__()

        # Initialize list of cards
        for suit in Suit:
            # create number cards
            for n in range(2,10):
                self.cards.append(Card(str(n), suit, n))
            # create face cards
            self.cards.append(Card(FaceCard.ACE.value, suit, 13))
            self.cards.append(Card(FaceCard.KING.value, suit, 12))
            self.cards.append(Card(FaceCard.QUEEN.value, suit, 11))
            self.cards.append(Card(FaceCard.JACK.value, suit, 10))

        # Create jokers
        if (jokers_included):
            self.cards.append(Card('Z', 'Z', 0, True))
            self.cards.append(Card('Z', 'Z', 0, True))

    # Shuffles deck of cards
    def shuffle(self):
        shuffle(self.cards)

    def isEmpty(self):
        return super(Deck, self).isEmpty()

    def numOfCards(self):
        return super(Deck, self).numOfCards()

    # Returns a tuple of information about the top card
    def checkTopCard(self):
        return super(Deck, self).checkTopCard()

    # Removes and then returns the top card
    def takeTop(self):
        return super(Deck, self).takeTop()

    def takeBottom(self):
        return super(Deck, self).takeBottom()

    # Adds a new card onto the stack of cards
    def put(self, card, faceUp=True):
        super(Deck, self).put(card, faceUp)

