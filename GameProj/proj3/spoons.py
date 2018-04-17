from common import *
from cardgame import CardGame
from cardpatterns import any_four_of_a_kind
from env import Env
from pile import Pile
from spoonsrules import SPOONS_RULES

class SpoonsEnv(Env):
    def __init__(self, deck_size, deck_w_jokers, num_players, start_hand_size, direction):
        super(SpoonsEnv, self).__init__(deck_size, deck_w_jokers, num_players, start_hand_size, direction)
        self.trash = Pile()
        self.pass_pile = Pile()
        self.end_player = num_players - 1


def spoons_win_cond(env):
    for player in env.players:
        if any_four_of_a_kind(player.hand):
            return True
    return False


SPOONS = {
    ENV: SpoonsEnv,
    DECK_SIZE: 1,
    DECK_W_JOKERS: False,
    NUM_PLAYERS: 5,
    START_HAND_SIZE: 4,
    DIRECTION: CLOCKWISE,
    GAME_RULES: SPOONS_RULES,
    WIN_COND: spoons_win_cond
}

CardGame(SPOONS).play()
