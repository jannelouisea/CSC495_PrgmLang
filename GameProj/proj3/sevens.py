from game import Game
from env import SevensEnv
from pile import Pile
from common import prompt_input
from card import Card
from enums import Suit

SEVENS_SUMMARY = '''
======================================================
                       Sevens
------------------------------------------------------
Bartok is a card game that uses a standard deck
without Jokers. The number of players can range from
2 to 5 players. The number of cards each player can
start with range from 5 to 7 cards.

The objective of the game is to be the first player
to get rid of all their cards.

You can only place cards from your hand to the Center
pile if they match either the rank or suit of the top
card in the Center pile or if they match a Draw2 Card
(rank 2).

When it is your turn, you have to chose which card
to place in the Center pile. If only one card can be
placed or if you can only draw card(s) from the deck,
the program will automatically act for you.

To transition between players, the next player has to
enter their position before proceeding.

Good Luck. Now let's play!
======================================================
'''

# https://www.wikihow.com/Play-the-Card-Game-Called-Sevens
class Sevens(Game):

    def __init__(self, game):
        super(Sevens, self).__init__(game)
        self.min_players = 3
        self.max_players = 8
        self.env[SevensEnv.spades_layout] = Pile()
        self.env[SevensEnv.diamonds_layout] = Pile()
        self.env[SevensEnv.clubs_layout] = Pile()
        self.env[SevensEnv.hearts_layout] = Pile()

    def winning_cond(self, player):
        return player.hand_size() == 0

    def show_table(self):
        table = {
            'SPADES': self.env[SevensEnv.spades_layout].cards,
            'DIAMONDS': self.env[SevensEnv.diamonds_layout].cards,
            'CLUBS': self.env[SevensEnv.clubs_layout].cards,
            'HEARTS': self.env[SevensEnv.hearts_layout].cards
        }

        print("=================================")
        print("              Table")
        print("---------------------------------")
        for suit, layout in table.items():
            print(f"{suit}: ", end="")
            if len(layout) == 0:
                print("[]")
            else:
                for card in layout:
                    print (f"{card} ", end="")
                print()
        print("=================================")

    def start(self):
        start_card = Card("7", Suit.DIAMONDS, 7)

        def start_card_cond(card):
            return card.matches_card(start_card)

        for index, player in enumerate(self.env[SevensEnv.players]):
            if player.has_card_w_criteria([start_card_cond]):
                self.env[SevensEnv.cur_player_pos] = index
                break

    def set_up(self):
        print("---------------------------------")
        print("Set Up")
        print("---------------------------------")
        self.set_norm_deck()
        num_players = self.ask_num_players(self.min_players, self.max_players)
        self.init_players_w_eq_cards(num_players)

    def play(self):
        print(SEVENS_SUMMARY)

        self.start()
        while self.env[SevensEnv.winner_pos] < 0:
            self.show_table()
            self.let_cur_player_play()
            self.check_winner(self.winning_cond)
