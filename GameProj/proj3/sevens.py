from game import Game
from env import SevensEnv
from pile import Pile
from card import Card
from enums import Suit

SEVENS_SUMMARY = '''
======================================================
                       Sevens
------------------------------------------------------
Bartok is a card game that uses a standard deck of
card without Jokers. The number of players can range
from 3 to 8 players.

The objective of the game is to be the first player
to get rid of all their cards.

Special Cards in the Game:
Start Card         - 7 Diamonds
Start Layout Card  - any card with rank 7 except Start Card

The player who has the 7 Diamonds goes first. Direction
is clockwise.

Each player can do one the following moves on their
turn:
1 - Play Start Layout Card
    When a player plays a Start Layout Card, this
    creates a new layout for that card's suit.

2 - Play Adjacent Card
    For one of the four layouts, the player can only
    put the next highest or lowest card.

3 - Knock (can't play anything)

If player can only play either one start layout card or
on adjacent card, then that card is automatically placed
in the corresponding layout. 

To transition between players, the next player has to
enter their position before proceeding.

Good Luck. Now let's play!
======================================================
'''


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
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

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def winning_cond(player):
        return player.hand_size() == 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
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
            print(f"{suit}: \t", end="")
            if suit == 'CLUBS':
                print('\t', end="")
            if len(layout) == 0:
                print("[]")
            else:
                for card in layout:
                    print(f"{card} ", end="")
                print()
        print("=================================")

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def find_start_player(self):
        start_card = Card("7", Suit.DIAMONDS, 7)

        def start_card_cond(card):
            return card.matches_card(start_card)

        for index, player in enumerate(self.env[SevensEnv.players]):
            if player.has_card_meet_cond(start_card_cond):
                self.env[SevensEnv.cur_player_pos] = index
                break

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def set_up(self):
        print("---------------------------------")
        print("Set Up")
        print("---------------------------------")
        self.set_norm_deck()
        num_players = self.ask_num_players(self.min_players, self.max_players)
        self.init_players_w_eq_cards(num_players)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def play(self):
        print(SEVENS_SUMMARY)

        self.find_start_player()
        while self.env[SevensEnv.winner_pos] < 0:
            self.show_table()
            self.let_cur_player_play()
            self.check_winner(self.winning_cond)
