from game import Game
from env import BartokEnv
from pile import Pile
from common import prompt_input

BARTOK_SUMMARY = '''
======================================================
                        Bartok
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


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class Bartok(Game):

    def __init__(self, game):
        super(Bartok, self).__init__(game)
        self.min_players = 2
        self.max_players = 5
        self.start_card_min = 5
        self.start_card_max = 7
        self.env[BartokEnv.center] = Pile()
        self.env[BartokEnv.draw2] = False
        self.env[BartokEnv.draw2_effect] = 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def winning_cond(self, player):
        return player.hand_size() == 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def num_cards_cond(self, num_cards):
        return not(int(num_cards) < self.start_card_min or int(num_cards) > self.start_card_max)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def set_up(self):
        print("---------------------------------")
        print("Set Up")
        print("---------------------------------")
        self.set_norm_deck()
        num_players = self.ask_num_players(self.min_players, self.max_players)

        num_cards_prompt = f'How many cards should each player start with? ' \
                           f'Must be between {self.start_card_min} or {self.start_card_max} cards.\n> '
        num_cards_err = 'ERROR: Incorrect number of start cards.'
        num_cards = int(prompt_input(num_cards_prompt, self.num_cards_cond, num_cards_err))

        self.init_players(num_players, num_cards)
        self.env[BartokEnv.center].put(self.env[BartokEnv.deck].take_top())

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def show_center_top_card(self):
        top_card = self.env[BartokEnv.center].look_top()
        print("=================================")
        print(f"Center Card: {top_card}")
        print("=================================")

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def play(self):
        print(BARTOK_SUMMARY)

        while self.env[BartokEnv.winner_pos] < 0:
            self.show_center_top_card()
            self.let_cur_player_play()
            self.check_winner(self.winning_cond)
