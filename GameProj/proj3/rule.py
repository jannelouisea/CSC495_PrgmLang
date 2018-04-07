from thing import Thing
from env import Env


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class Rule(Thing):

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def __init__(self, player):
        self.player = player
        self.env = player.env

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def change_curr_player(self, jump_size, skips):
        self.env[Env.rec_player_pos] = self.env[Env.cur_player_pos]
        self.env[Env.cur_player_pos] = self.next_player(jump_size, skips)

    # ------------------------------------------------------------------------------------------------- #
    # Determines the next player in a circle of players.                                                #
    #                                                                                                   #
    # Each turn is assumed to go the next person on the right or left                                   #
    # depending on the play direction. Skips that are done in a linear fashion                          #
    # are also accounted for.                                                                           #
    #                                                                                                   #
    # :param player: The current player                                                                 #
    # :param jump_size: ...                                                                             #
    # :param skips: Number of skips                                                                     #
    # :return: The index of the next player                                                             #
    # ------------------------------------------------------------------------------------------------- #
    def next_player(self, jump_size, skips):
        curr_player_pos = self.env[Env.cur_player_pos]
        direction = self.env[Env.direction]
        num_players = self.env[Env.num_players]
        last_idx = num_players - 1

        next_player = curr_player_pos + (direction * ((jump_size * (skips + 1)) % num_players))

        if next_player < 0 or next_player > last_idx:
            next_player -= direction * num_players

        return next_player

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        pass

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        pass
