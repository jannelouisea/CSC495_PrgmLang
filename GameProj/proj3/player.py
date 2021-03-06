from card import Card
from thing import Thing


class Player(Thing):
    def __init__(self, pos, env):
        self.env = env
        self.hand = list()
        self.pos = pos
        # self.game_rules = {i: rule(env) for i, rule in enumerate(game_rules)}
        self.game_rules = {}
        self.norm_pos = self.pos + 1

    def __str__(self):
        self_str = f"{self.pos} -"
        for card in self.hand:
            self_str += f" {card}"
        return self_str

    def hand_size(self):
        return len(self.hand)

    def add_to_hand(self, card, face_up=True):
        if isinstance(card, Card):
            if card.face_up != face_up:
                card.flip()
            self.hand.append(card)

    def hand_to_str(self):
        hand = ""
        for card in self.hand:
            hand += card.rank
        for card in self.hand:
            hand += card.suit.value
        return hand

    def rmv_from_hand(self, idx):
        return self.hand.pop(idx)

    def sort_hand(self, sort_func):
        self.hand = sort_func(self.hand)

    def show_hand(self, info_funcs=None):
        num_cols = 4
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
        print("Your Hand (index - card)")
        for index, card in enumerate(self.hand):
            print(f"{index} - {card}\t", end="")
            if (index + 1) % num_cols == 0 and not index == self.hand_size() - 1:
                print()
        print("\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

    def has_card_meet_cond(self, cond):
        for card in self.hand:
            if cond(card):
                return True
        return False

    def default_cond(self, card):
        return True

    def cards_meet_cond(self, cond=None):
        if not cond:
            cond = lambda x: x == x # Always evaluates to true
        return [index for index, card in enumerate(self.hand) if cond(card)]

    def possible_actions(self):
        return [(i, self.game_rules[i].name.value) for i in self.game_rules if self.game_rules[i].can_act(self)]

    def act(self, desired_action):
        self.game_rules[desired_action].act(self)
