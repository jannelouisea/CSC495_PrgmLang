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
