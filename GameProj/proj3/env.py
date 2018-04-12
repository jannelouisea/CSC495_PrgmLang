from thing import Thing
from deck import Deck
from copy import deepcopy

class Env(Thing):

    __shared_state = {}
    __saved_state = {}

    def __init__(self, deck_size, deck_w_jokers, num_players, start_hand_size, direction):
        self.__dict__ = self.__shared_state
        self.deck = Deck(deck_size, deck_w_jokers)
        self.num_players = num_players
        self.players = self.init_players(num_players, start_hand_size)
        self.cur_player_pos = 0
        self.rec_player_pos = 0
        self.direction = direction
        self.winner_pos = -1

    def init_players(self, num_players, start_hand_size):
        players = []
        return players

    def save(self):
        self.__saved_state = self.__shared_state

    def revert(self):
        self.__shared_state = self.__saved_state

    def snapshot(self):
        return deepcopy(self.__shared_state)


'''
class Env:
    deck = 'deck'
    players = 'players'
    num_players = 'num_players'
    start_players_pos = 'start_player_pos'
    rec_player_pos = 'rec_player_pos'
    cur_player_pos = 'cur_player_pos'
    direction = 'direction'
    winner_pos = 'winner_pos'


class BartokEnv(Env):
    center = 'center'
    draw2 = 'draw2'
    draw2_effect = 'draw2_effect'


class SpoonsEnv(Env):
    trash = 'trash'
    end_player = 'end_player'


class SevensEnv(Env):
    spades_layout = 'spades_layout'
    diamonds_layout = 'diamonds_layout'
    clubs_layout = 'clubs_layout'
    hearts_layout = 'hearts_layout'
'''
