from common import *
from sevensrules import SEVENS_RULES
from cardgame import CardGame
from pile import Pile
from env import Env
from enums import Suit


class SevensEnv(Env):
    def __init__(self, deck_size, deck_w_jokers, num_players, start_hand_size, direction):
        super(SevensEnv, self).__init__(deck_size, deck_w_jokers, num_players, start_hand_size, direction)
        self.spades_layout = Pile()
        self.diamonds_layout = Pile()
        self.clubs_layout = Pile()
        self.hearts_layout = Pile()


def sevens_set_up(env):
    def start_card_cond(card):
        return card.matches_rank('7') and card.matches_suit(Suit.DIAMONDS)

    for index, player in enumerate(env.players):
        if player.has_card_meet_cond(start_card_cond):
            env.cur_player_pos = index
            break


def sevens_pre_player_turn(env):
    table = {
        'SPADES': env.spades_layout.cards,
        'DIAMONDS': env.diamonds_layout.cards,
        'CLUBS': env.clubs_layout.cards,
        'HEARTS': env.hearts_layout.cards
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


def sevens_winning_cond(env):
    for player in env.players:
        if player.hand_size() == 0:
            return True
    return False


SEVENS = {
    ENV: SevensEnv,
    DECK_SIZE: 1,
    DECK_W_JOKERS: False,
    NUM_PLAYERS: 3,
    START_HAND_SIZE: EQUAL_NUM_CARDS,
    DIRECTION: CLOCKWISE,
    GAME_RULES: SEVENS_RULES,
    SETUP: sevens_set_up,
    PRE_PLAYER_TURN: sevens_pre_player_turn,
    WINNING_COND: sevens_winning_cond
}

CardGame(SEVENS).play()
