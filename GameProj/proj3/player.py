from card import Card
from bartokrules import BartokRules
from sevensrules import SevensRules
from spoonsrules import SpoonsRules
from enums import Game


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class Player:
    def __init__(self, env, pos, game):
        def deter_rules(player, game_inst):
            if game_inst == Game.BARTOK:
                return BartokRules(player).rules_map
            if game_inst == Game.SEVENS:
                return SevensRules(player).rules_map
            # Other rules from different games would go here
            if game_inst == Game.SPOONS:
                return SpoonsRules(player).rules_map

        self.env = env
        self.hand = list()
        self.pos = pos
        self.rules_map = deter_rules(self, game)
        self.norm_pos = self.pos + 1

    def __str__(self):
        self_str = f"{self.pos} -"
        for card in self.hand:
            self_str += f" {card}"
        return self_str

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def hand_size(self):
        return len(self.hand)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def add_to_hand(self, card, face_up=True):
        if isinstance(card, Card):
            if card.face_up != face_up:
                card.flip()
            self.hand.append(card)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def hand_to_str(self):
        hand = ""
        for card in self.hand:
            hand += card.rank
        for card in self.hand:
            hand += card.suit.value
        return hand

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def rmv_from_hand(self, idx):
        return self.hand.pop(idx)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def sort_hand(self, sort_func):
        self.hand = sort_func(self.hand)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def show_hand(self, info_funcs=None):
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
        print("Your Hand (index - card)")
        for index, card in enumerate(self.hand):
            print(f"{index} - {card}\t", end="")
            if (index + 1) % 2 == 0:
                print()
        print("\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def has_card_meet_cond(self, cond):
        for card in self.hand:
            if cond(card):
                return True
        return False

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def cards_meet_cond(self, cond):
        return [index for index, card in enumerate(self.hand) if cond(card)]

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def cards_in_hand(self):
        return [index for index, card in enumerate(self.hand)]

    def reflect(self):
        i = 1
        for card in self.hand:
            print("Card {}: {} of {}".format(i, card.rank, card.suit))
            i += 1

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def possible_actions(self):
        return [(i, self.rules_map[i].name.value) for i in self.rules_map if self.rules_map[i].can_act()]

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self, desired_action):
        self.rules_map[desired_action].act()
