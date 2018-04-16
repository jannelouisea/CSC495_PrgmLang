from thing import Thing
from deck import Deck
from copy import deepcopy
from common import EQUAL_NUM_CARDS
from cardpatterns import sort_cards
from player import Player

class Env(Thing):

    __shared_state = {}
    __saved_state = {}

    def __init__(self, deck_size, deck_w_jokers, num_players, start_hand_size, game_rules, direction):
        self.__dict__ = self.__shared_state
        self.deck = Deck(deck_size, deck_w_jokers)
        self.deck.shuffle()
        self.num_players = num_players
        self.players = self.init_players(num_players, start_hand_size, game_rules)
        self.cur_player_pos = 0
        self.rec_player_pos = 0
        self.direction = direction
        self.winner_pos = -1

    def init_players(self, num_players, start_hand_size, game_rules):
        players = [Player(i, self, game_rules) for i in range(num_players)]

        num_cards = start_hand_size * num_players
        if start_hand_size == EQUAL_NUM_CARDS:
            num_cards = self.deck.num_cards()

        for i in range(num_cards):
            players[i % num_players].add_to_hand(self.deck.take_top())

        for player in players:
            player.sort_hand(sort_cards)

        return players

    def get_cur_player(self):
        return self.players[self.cur_player_pos]

    def get_rec_player(self):
        return self.players[self.rec_player_pos]

    def found_winner(self):
        return self.winner_pos >= 0

    def save(self):
        self.__saved_state = deepcopy(self.__shared_state)

    def revert(self):
        self.__shared_state = deepcopy(self.__saved_state)

    def snapshot(self):
        return deepcopy(self.__shared_state)


'''
class SpoonsEnv(Env):
    trash = 'trash'
    end_player = 'end_player'


class SevensEnv(Env):
    spades_layout = 'spades_layout'
    diamonds_layout = 'diamonds_layout'
    clubs_layout = 'clubs_layout'
    hearts_layout = 'hearts_layout'
'''
