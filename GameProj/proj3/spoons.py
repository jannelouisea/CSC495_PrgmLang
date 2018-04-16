from game import Game
from env import SpoonsEnv
from env import Env
from card_patterns import any_four_of_a_kind
from pile import Pile

SPOONS_SUMMARY = '''
Let's play Spoons!
Spoons Requirements:
A standard deck of cards (without Jokers)
3 to 13 players
Game Play:
The first person with four matching cards wins.
Each player is dealt four cards.
The dealer (Player 1) takes a card off the top of the deck to have five cards in their hand
They remove one card and pass it to the left.
Each person discards to the person on the left.
If you are the last player, you discard to the trash pile.
If the deck ever runs out, the trash pile is shuffled and replaces the deck.
If you have four matching cards in your hand, you must discard the fifth non-matching card to win the game.
'''


class Spoons(Game):

    def __init__(self, game):
        super(Spoons, self).__init__(game)
        self.name = 'Spoons'
        self.min_players = 3
        self.max_players = 13
        self.init_hand_size = 4
        self.env[SpoonsEnv.trash] = Pile()
        self.env[SpoonsEnv.end_player] = 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def winning_cond(self, player):
        return any_four_of_a_kind(player.hand)

    @staticmethod
    def num_player_cond(num_players):
        return not(int(num_players) < 3 or int(num_players) > 13)

    def set_up(self):
        print("Setting up Spoons...")
        self.set_norm_deck()
        self.env[SpoonsEnv.pass_pile] = Pile()
        num_players = self.ask_num_players(self.min_players, self.max_players)
        self.init_players(num_players, 4)
        self.env[SpoonsEnv.end_player] = num_players - 1

    def play(self):
        print(SPOONS_SUMMARY)
        while self.env[SpoonsEnv.winner_pos] < 0:
            self.let_cur_player_play()
            self.check_winner(self.winning_cond)
