from env import Env
from pile import Pile


class BartokEnv(Env):
    def __init__(self, deck_size, deck_w_jokers, num_players, start_hand_size, rules_map, direction):
        super(BartokEnv, self).__init__(deck_size, deck_w_jokers, num_players, start_hand_size, rules_map, direction)
        self.center = Pile()
        self.draw2 = False
        self.draw2_effect = 0
