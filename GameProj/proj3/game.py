from thing import Thing
from player import Player
import sys
from deck import Deck
from env import Env
from enums import Direction
from common import prompt_input


class Game(Thing):
    def __init__(self, game):
        self.game = game
        self.name = ""
        self.env = {
            Env.deck: Deck(True),
            Env.players: list(),
            Env.rec_player_pos: 0,
            Env.cur_player_pos: 0,
            Env.direction: Direction.CLOCKWISE,
            Env.winner_pos: -1
        }

    def set_norm_deck(self):
        self.env[Env.deck] = Deck()       # Deck without Jokers
        self.env[Env.deck].shuffle()

    def set_deck_w_jokers(self):
        self.env[Env.deck] = Deck(True)       # Deck without Jokers
        self.env[Env.deck].shuffle()

    def let_user_choose_deck(self):
        def deck_cond(x):
            return x == 0 or x == 1

        deck_prompt = 'Choose deck type.\n0 - Without Jokers\n1 - With Jokers'
        deck_err = 'Please enter 0 or 1.'
        prompt_input(deck_prompt, deck_cond, None, deck_err, None)

    def ask_num_players(self, min_num, max_num):
        def num_player_cond(num_players):
            return not(int(num_players) < min_num or int(num_players) > max_num)

        num_player_prompt = f"How many players? Number must be between {min_num} and {max_num}.\n> "
        num_player_err = 'ERROR: Incorrect number of players.'
        num_players = int(prompt_input(num_player_prompt, num_player_cond, None, num_player_err, None))
        self.env[Env.num_players] = num_players
        return num_players

    def init_players(self, num_players, num_cards=0):
        for i in range(0, num_players):
            player = Player(self.env, i, self.game)
            for j in range(num_cards):
                player.add_to_hand(self.env[Env.deck].take_top())
            self.env[Env.players].append(player)

    def cur_player(self):
        return self.env[Env.players][self.env[Env.cur_player_pos]]

    def play(self): pass

    def set_up(self): pass

    def det_winner(self): pass
