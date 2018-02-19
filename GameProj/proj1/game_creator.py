from deck import Deck

deck_no_jokers = Deck()       # Creates a standard 52 deck WITHOUT jokers
deck_w_jokers = Deck(True)       # Creates a standard 52 deck WITHOUT jokers

if __name__ == '__main__':
    print(deck_no_jokers.__repr__())
    print('===================')
    print(deck_w_jokers.__repr__())
