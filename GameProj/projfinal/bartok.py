from common import *
from bartokrules import BARTOK_RULES
from cardgame import CardGame
from env import Env
from pile import Pile
from sys import stderr


class BartokEnv(Env):
    def __init__(self, deck_size, deck_w_jokers, deck_wo_queens, num_players, start_hand_size, direction):
        super(BartokEnv, self).__init__(deck_size, deck_w_jokers, deck_wo_queens, num_players, start_hand_size, direction)
        self.center = Pile()
        self.draw2 = False
        self.draw2_effect = 0


def bartok_setup(env):
    if env.deck.is_empty():
        print('ERROR: Deck is empty. Cannot place card in center pile.', file=stderr)
        exit()  # TODO Throw exception instead of exiting
    env.center.put(env.deck.take_top())


def bartok_pre_player_turn(env):
    top_card = env.center.look_top()
    print("=================================")
    print(f"Center Card: {top_card}")
    print("=================================")


BARTOK = {
    ENV: BartokEnv,
    DECK_SIZE: 1,
    DECK_W_JOKERS: False,
    DECK_WO_QUEENS: False,
    NUM_PLAYERS: 3,
    START_HAND_SIZE: 5,
    DIRECTION: CLOCKWISE,
    GAME_RULES: BARTOK_RULES,
    SETUP: bartok_setup,
    PRE_PLAYER_TURN: bartok_pre_player_turn,
    WIN_COND: empty_hand_win_cond
}

CardGame(BARTOK).play()
