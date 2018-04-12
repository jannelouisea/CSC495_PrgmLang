from thing import Thing

class Env(Thing):

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

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
