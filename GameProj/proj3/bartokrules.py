from rule import Rule
from enums import BartokRuleEnum
from gamerules import GameRules
from env import BartokEnv


# ------------------------------------------------------------------------------------------------- #
# The set of rules for Bartok.                                                                      #
#                                                                                                   #
# :attribute rules: A list of BartokRules.                                                          #
# :attribute rules_map: A mapping on BartokRules where the key is the position of the rule in       #
#                       rules, and the value is the rule.                                           #
# ------------------------------------------------------------------------------------------------- #
class BartokRules(GameRules):
    def __init__(self, player):
        super().__init__(player)
        self.rules = [Draw2Rule(player), PlayDraw2Rule(player),
                      PlaySkipRule(player), PlayReverseRule(player),
                      PlayMatchRule(player), DrawCardRule(player)]
        self.rules_map = {i: val for i, val in enumerate(self.rules)}


# ------------------------------------------------------------------------------------------------- #
# The parent class for each rule in Bartok.                                                         #
# The class contains Bartok related functions used in multiple rules.                               #
# ------------------------------------------------------------------------------------------------- #
class BartokRule(Rule):
    def __init__(self, player):
        super().__init__(player)

    # ------------------------------------------------------------------------------------------------- #
    # Checks if the current card meets the skip card condition. (rank 7)                                #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def skip_card_cond(card):
        return card.matches_rank('7')

    # ------------------------------------------------------------------------------------------------- #
    # Checks if the current card meets the reverse card condition. (rank 8)                             #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def reverse_card_cond(card):
        return card.matches_rank('8')

    # ------------------------------------------------------------------------------------------------- #
    # Checks if the current card meets the skip card condition. (rank 2)                                #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def draw2_card_cond(card):
        return card.matches_rank('2')

    # ------------------------------------------------------------------------------------------------- #
    # Checks if the current deck is empty and refills the deck from the center pile if the deck is      #
    # empty.                                                                                            #
    # ------------------------------------------------------------------------------------------------- #
    def check_deck(self):
        deck = self.env[BartokEnv.deck]
        center = self.env[BartokEnv.center]

        if deck.is_empty():
            add_count = center.num_cards() - 1
            for i in range(0, add_count):
                deck.put(center.take_bottom(), False)

    # ------------------------------------------------------------------------------------------------- #
    # Given n a number of cards, n cards are taken from the deck and added to the player's hand.        #
    #                                                                                                   #
    # :param num_cards: Number of cards, default value is 1.                                            #
    # :param show: Boolean value to determine if the cards added are shown on the screen, default       #
    #               value set to True.                                                                  #
    # ------------------------------------------------------------------------------------------------- #
    def add_to_hand_from_deck(self, num_cards=1, show=True):
        added = list()
        self.check_deck()
        for i in range(num_cards):
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
    # Shows what the player placed in the center pile.                                                  #
    # ------------------------------------------------------------------------------------------------- #
    def play_recap(self):
        top_card = self.env[BartokEnv.center].look_top()
        player = self.env[BartokEnv.cur_player_pos]
        print(f"Player {player} played {top_card}.")


# ------------------------------------------------------------------------------------------------- #
# Bartok's Draw 2 Rule                                                                              #
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
        print(f"You cannot play any cards. Automatically adding {draw_count} cards to your hand.")
        self.add_to_hand_from_deck(draw_count)
        self.reset_draw2_effect()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
# Bartok's Draw 2 Rule                                                                              #
# ------------------------------------------------------------------------------------------------- #
class PlayDraw2Rule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.PLAYDRAW2

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
        return self.player.has_card_meet_cond(self.draw2_card_cond)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        draw2_cards = self.player.cards_meet_cond(self.draw2_card_cond)
        draw2_card = draw2_cards[0] if len(draw2_cards) == 1 else self.user_choose_card(draw2_cards, "draw2")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(draw2_card))
        self.inc_draw2_effect()
        self.play_recap()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# Bartok's Draw 2 Rule                                                                              #
# ------------------------------------------------------------------------------------------------- #
class PlaySkipRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.PLAYSKIP
        self.draw2_rule = Draw2Rule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.draw2_rule.can_act()) and self.player.has_card_meet_cond(self.skip_card_cond)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        skip_cards = self.player.cards_meet_cond(self.skip_card_cond)
        skip_card = skip_cards[0] if len(skip_cards) == 1 else self.user_choose_card(skip_cards, "skip")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(skip_card))
        self.play_recap()
        self.change_curr_player(1, 1)


# ------------------------------------------------------------------------------------------------- #
# Bartok's Draw 2 Rule                                                                              #
# ------------------------------------------------------------------------------------------------- #
class PlayReverseRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.PLAYREVERSE
        self.draw2_rule = Draw2Rule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.draw2_rule.can_act()) and self.player.has_card_meet_cond(self.reverse_card_cond)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        reverse_cards = self.player.cards_meet_cond(self.reverse_card_cond)
        reverse_card = reverse_cards[0] if len(reverse_cards) == 1 else self.user_choose_card(reverse_cards, "reverse")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(reverse_card))
        self.env[BartokEnv.direction] *= -1
        self.play_recap()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
# Bartok's                                                                                          #
# ------------------------------------------------------------------------------------------------- #
class PlayMatchRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.PLAYMATCHCARD
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
        return (not self.draw2_rule.can_act()) and self.player.has_card_meet_cond(self.place_match_cond)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        matched_cards = self.player.cards_meet_cond(self.place_match_cond)
        matched_card = matched_cards[0] if len(matched_cards) == 1 else self.user_choose_card(matched_cards, "matched")
        self.env[BartokEnv.center].put(self.player.rmv_from_hand(matched_card))
        self.play_recap()
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
# Bartok's Draw 2 Rule                                                                              #
# ------------------------------------------------------------------------------------------------- #
class DrawCardRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.DRAWCARD
        self.draw2_rule = Draw2Rule(player)
        self.place_draw2_rule = PlayDraw2Rule(player)
        self.skip_rule = PlaySkipRule(player)
        self.reverse_rule = PlayReverseRule(player)
        self.place_match_rule = PlayMatchRule(player)

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
        print("You cannot play any cards. Automatically adding one card to your hand.")
        self.add_to_hand_from_deck()
        self.change_curr_player(1, 0)
