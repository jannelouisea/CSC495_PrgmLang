from enums import Suit
from deck import Deck

# https://stackoverflow.com/questions/37179737/sorting-list-of-cards
rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']
suit_order_asc = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
suit_map = {val: i for i, val in enumerate(suit_order_asc)}


def sort_cards(cards, desc=False):
    return sorted(cards, key=lambda card: (suit_map[card.suit], card.value), reverse=desc)


def group_cards(cards, desc=False):
    return sorted(cards, key=lambda card: card.value, reverse=desc)


def cards_to_str(cards):
    cards_str = ""
    for card in cards:
        cards_str += card.rank
    for card in cards:
        cards_str += card.suit.value
    return cards_str


def four_of_a_kind(cards, kind):
    cards = group_cards(cards)
    cards_str = cards_to_str(cards)
    pattern = f"{kind}{kind}{kind}{kind}"
    return cards_str.find(pattern) >= 0


def any_four_of_a_kind(cards):
    return [rank for rank in rank_order if four_of_a_kind(cards, rank)]
