from thing import Thing
from card import Card
from bartokrules import BartokRules
from enums import Game


class Player():
    def __init__(self, env, pos, game):
        def deter_rules(player, game_inst):
            if game_inst == Game.BARTOK:
                return BartokRules(player)
            # Other rules from different games would go here

        self.env = env
        self.hand = list()
        self.pos = pos
        self.game_rules = deter_rules(self, game)
        self.move = None
        self.norm_pos = self.pos + 1

    def __str__(self):
        return f"{self.pos} {self.hand_to_str()}"

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

    def show_hand(self, info_funcs):
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
        print("Your Hand (index - card)")
        for index, card in enumerate(self.hand):
            print(f"{index} - {card} ", end="")
            for info_cond, info_msg in info_funcs:
                if info_cond(card):
                    print(f"{info_msg} ", end="")
            print()
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

    def cards_meet_criteria(self, criteria):
        cards = list()
        for index, card in enumerate(self.hand):
            for cond in criteria:
                if cond(card):
                    cards.append(index)
        return cards

    def reflect(self):
        i = 1
        for card in self.hand:
            print("Card {}: {} of {}".format(i, card.rank, card.suit))
            i += 1

    def weigh_actions(self):
        for rule in self.game_rules.rules:
            if rule.can_act():
                self.move = rule
                break

    def act(self):
        self.move.act()
