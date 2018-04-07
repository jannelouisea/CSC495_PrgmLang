from rule import Rule
from enums import BartokRuleEnum
from gamerules import GameRules
from env import BartokEnv
from common import prompt_input


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class BartokRules(GameRules):
    def __init__(self, player):
        super().__init__(player)
        self.rules = [Draw2Rule(player), PlaceDraw2Rule(player),
                      SkipRule(player), ReverseRule(player),
                      PlaceMatchRule(player), DrawCardRule(player)]
        self.rules_map = {i: val for i, val in enumerate(self.rules)}


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class BartokRule(Rule):
    def __init__(self, player):
        super().__init__(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def skip_card_cond(card):
        return card.matches_rank('7')

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def reverse_card_cond(card):
        return card.matches_rank('8')

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def draw2_card_cond(card):
        return card.matches_rank('2')

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def check_deck(self):
        deck = self.env[BartokEnv.deck]
        center = self.env[BartokEnv.center]

        if deck.is_empty():
            add_count = center.num_cards() - 1
            for i in range(0, add_count):
                deck.put(center.take_bottom(), False)

    # TODO: Put into rule if other games need this functionality
    # TODO: Abstract check_deck() ?
    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def add_to_hand_from_deck(self, count=1, show=True):
        added = list()
        self.check_deck()
        for i in range(count):
            added_card = self.env[BartokEnv.deck].take_top()
            self.player.add_to_hand(added_card)
            added.append(added_card)
            self.check_deck()
        if show:
            msg = "Added to hand:"
            for card in added:
                msg += f" {card}"
            print(msg)
        return added

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def user_choose_card(self, valid_cards, card_type=''):
        def valid_card(idx):
            return int(idx) in valid_cards

        choose_card_prompt = f"Enter the index of the {card_type} card would you like to play.\nIndex - Card\n"
        for card in valid_cards:
            choose_card_prompt += f"{card} - {self.player.hand[card]}\n"
        choose_card_prompt += "> "
        choose_card_err = "Invalid index."
        return int(prompt_input(choose_card_prompt, valid_card, choose_card_err))

    def play_recap(self):
        top_card = self.env[BartokEnv.center].look_top()
        player = self.env[BartokEnv.cur_player_pos]
        print(f"Player {player} played {top_card}.")


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class Draw2Rule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.DRAW2

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def reset_draw2_effect(self):
        self.env[BartokEnv.draw2] = False
        self.env[BartokEnv.draw2_effect] = 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def draw2_count(self):
        return self.env[BartokEnv.draw2_effect] * 2

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return self.env[BartokEnv.draw2]

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        draw_count = self.draw2_count()
        print(f"Automatically adding {draw_count} cards to your hand.")
        self.add_to_hand_from_deck(draw_count)
        self.reset_draw2_effect()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class PlaceDraw2Rule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.PLACEDRAW2

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def inc_draw2_effect(self):
        self.env[BartokEnv.draw2] = True
        self.env[BartokEnv.draw2_effect] += 1

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return self.player.has_card_w_criteria([self.draw2_card_cond])

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        draw2_cards = self.player.cards_meet_criteria([self.draw2_card_cond])
        draw2_card = draw2_cards[0] if len(draw2_cards) == 1 else self.user_choose_card(draw2_cards, "draw2")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(draw2_card))
        self.inc_draw2_effect()
        self.play_recap()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class SkipRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.SKIP
        self.draw2_rule = Draw2Rule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.draw2_rule.can_act()) and self.player.has_card_w_criteria([self.skip_card_cond])

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        skip_cards = self.player.cards_meet_criteria([self.skip_card_cond])
        skip_card = skip_cards[0] if len(skip_cards) == 1 else self.user_choose_card(skip_cards, "skip")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(skip_card))
        self.play_recap()
        self.change_curr_player(1, 1)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class ReverseRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.REVERSE
        self.draw2_rule = Draw2Rule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.draw2_rule.can_act()) and self.player.has_card_w_criteria([self.reverse_card_cond])

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        reverse_cards = self.player.cards_meet_criteria([self.reverse_card_cond])
        reverse_card = reverse_cards[0] if len(reverse_cards) == 1 else self.user_choose_card(reverse_cards, "reverse")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(reverse_card))
        self.env[BartokEnv.direction] *= -1
        self.play_recap()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class PlaceMatchRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.PLACEMATCHCARD
        self.draw2_rule = Draw2Rule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def place_match_cond(self, card):
        center_card = self.env[BartokEnv.center].look_top()
        return (not self.skip_card_cond(card)) and \
               (not self.reverse_card_cond(card)) and \
               (not self.draw2_card_cond(card)) and \
               (card.matches_rank(center_card.rank) or card.matches_suit(center_card.suit))

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.draw2_rule.can_act()) and self.player.has_card_w_criteria([self.place_match_cond])

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        matched_cards = self.player.cards_meet_criteria([self.place_match_cond])
        matched_card = matched_cards[0] if len(matched_cards) == 1 else self.user_choose_card(matched_cards, "matched")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(matched_card))
        self.play_recap()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class DrawCardRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.DRAWCARD
        self.draw2_rule = Draw2Rule(player)
        self.place_draw2_rule = PlaceDraw2Rule(player)
        self.skip_rule = SkipRule(player)
        self.reverse_rule = ReverseRule(player)
        self.place_match_rule = PlaceMatchRule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.draw2_rule.can_act()) and \
               (not self.place_draw2_rule.can_act()) and \
               (not self.skip_rule.can_act()) and \
               (not self.reverse_rule.can_act()) and \
               (not self.place_match_rule.can_act())

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        print("Automatically adding one card to your hand.")
        self.add_to_hand_from_deck()
        self.change_curr_player(1, 0)
