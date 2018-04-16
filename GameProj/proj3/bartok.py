from common import *
from bartokenv import BartokEnv
from bartokrules import BARTOK_RULES
from cardgame import CardGame


def bartok_setup(env):
    env.center.put(env.deck.take_top())


def bartok_pre_player_turn(env):
    top_card = env.center.look_top()
    print("=================================")
    print(f"Center Card: {top_card}")
    print("=================================")


def bartok_winning_cond(env):
    for player in env.players:
        if player.hand_size() == 0:
            return True
    return False


BARTOK = {
    ENV: BartokEnv,
    DECK_SIZE: 1,
    DECK_W_JOKERS: False,
    NUM_PLAYERS: 3,
    START_HAND_SIZE: 5,
    DIRECTION: CLOCKWISE,
    GAME_RULES: BARTOK_RULES,
    SETUP: bartok_setup,
    PRE_PLAYER_TURN: bartok_pre_player_turn,
    WINNING_COND: bartok_winning_cond
}

CardGame(BARTOK).play()
