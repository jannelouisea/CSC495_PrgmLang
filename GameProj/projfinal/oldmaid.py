from common import *
from cardgame import CardGame
from cardpatterns import any_four_of_a_kind
from env import Env
from pile import Pile
from oldmaidrules import OLDMAID_RULES


class OldmaidEnv(Env):
    def __init__(self, deck_size, deck_w_jokers, deck_wo_queens, num_players, start_hand_size, direction):
        super(OldmaidEnv, self).__init__(deck_size, deck_w_jokers, deck_wo_queens, num_players, start_hand_size, direction)
        self.trash = Pile()
        self.pass_pile = Pile()


def spoons_win_cond(env):
    for player in env.players:
        if any_four_of_a_kind(player.hand):
            return True
    return False


OLDMAID = {
    ENV: OldmaidEnv,
    DECK_SIZE: 1,
    DECK_W_JOKERS: False,
    DECK_WO_QUEENS: True,
    NUM_PLAYERS: 2,
    START_HAND_SIZE: 24,
    DIRECTION: CLOCKWISE,
    GAME_RULES: OLDMAID_RULES,
    WIN_COND: empty_hand_win_cond
}

CardGame(OLDMAID).play()
