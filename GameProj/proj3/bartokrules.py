from rule import Rule
from enums import BartokRuleEnum


class BartokRule(Rule):

    @staticmethod
    def skip_card_cond(card, env=None):
        return card.matches_rank('7')

    @staticmethod
    def reverse_card_cond(card, env=None):
        return card.matches_rank('8')

    @staticmethod
    def draw2_card_cond(card, env=None):
        return card.matches_rank('2')

    @staticmethod
    def check_deck(deck, center):
        if deck.is_empty():
            add_count = center.num_cards() - 1
            for i in range(0, add_count):
                deck.put(center.take_bottom(), False)

    def add_to_hand_from_deck(self, player, env, num_cards=1, show=True):
        added = list()
        self.check_deck(env.deck, env.center)
        for i in range(num_cards):
            added_card = env.deck.take_top()
            player.add_to_hand(added_card)
            added.append(added_card)
            self.check_deck(env.deck, env.center)
        if show:
            msg = "Added to hand:"
            for card in added:
                msg += f" {card}"
            print(msg)
        return added

    @staticmethod
    def recap(env):
        print(f"Player {env.get_cur_player().pos} played {env.center.look_top()}.")


class Draw2Rule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.DRAW2

    @staticmethod
    def reset_draw2_effect(env):
        env.draw2 = False
        env.draw2_effect = 0

    @staticmethod
    def draw2_count(env):
        return env.draw2_effect * 2

    def can_act(self, player, env):
        return env.draw2

    def act(self, player, env):
        draw_count = self.draw2_count(env)
        print(f"You cannot play any cards. Automatically adding {draw_count} cards to your hand.")
        self.add_to_hand_from_deck(player, env, draw_count)
        self.reset_draw2_effect(env)
        self.change_cur_player(env, 1, 0)


class PlayDraw2Rule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.PLAYDRAW2

    @staticmethod
    def inc_draw2_effect(env):
        env.draw2 = True
        env.draw2_effect += 1

    def can_act(self, player, env):
        return player.has_card_meet_cond(self.draw2_card_cond)

    def act(self, player, env):
        draw2_cards = player.cards_meet_cond(self.draw2_card_cond)
        draw2_card = draw2_cards[0] if len(draw2_cards) == 1 else self.user_choose_card(player, draw2_cards, "draw2")
        env.center.put(player.rmv_from_hand(draw2_card))
        self.inc_draw2_effect(env)
        print(f"Player {env.get_cur_player().pos} played {env.center.look_top()}. (Draw2 Card)")
        self.change_cur_player(env, 1, 0)


class PlaySkipRule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.PLAYSKIP
        self.draw2_rule = Draw2Rule()

    def can_act(self, player, env):
        return (not self.draw2_rule.can_act(player, env)) and player.has_card_meet_cond(self.skip_card_cond)

    def act(self, player, env):
        skip_cards = player.cards_meet_cond(self.skip_card_cond)
        skip_card = skip_cards[0] if len(skip_cards) == 1 else self.user_choose_card(player, skip_cards, "skip")
        env.center.put(player.rmv_from_hand(skip_card))
        print(f"Player {env.get_cur_player().pos} played {env.center.look_top()}. (Skip Card)")
        self.change_cur_player(env, 1, 1)


class PlayReverseRule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.PLAYREVERSE
        self.draw2_rule = Draw2Rule()

    def can_act(self, player, env):
        return (not self.draw2_rule.can_act(player, env)) and player.has_card_meet_cond(self.reverse_card_cond)

    def act(self, player, env):
        reverse_cards = player.cards_meet_cond(self.reverse_card_cond)
        reverse_card = reverse_cards[0] if len(reverse_cards) == 1 else self.user_choose_card(player, reverse_cards, "reverse")
        env.center.put(player.rmv_from_hand(reverse_card))
        env.direction *= -1
        print(f"Player {env.get_cur_player().pos} played {env.center.look_top()}. (Reverse Card)")
        self.change_cur_player(env, 1, 0)


class PlayMatchRule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.PLAYMATCHCARD
        self.draw2_rule = Draw2Rule()

    def place_match_cond(self, card, env):
        center_card = env.center.look_top()

        return (not self.skip_card_cond(card)) and \
               (not self.reverse_card_cond(card)) and \
               (not self.draw2_card_cond(card)) and \
               (card.matches_rank(center_card.rank) or card.matches_suit(center_card.suit))

    def can_act(self, player, env):
        return (not self.draw2_rule.can_act(player, env)) and player.has_card_meet_cond(self.place_match_cond)

    def act(self, player, env):
        matched_cards = player.cards_meet_cond(self.place_match_cond)
        matched_card = matched_cards[0] if len(matched_cards) == 1 else self.user_choose_card(player, matched_cards, "matched")
        env.center.put(player.rmv_from_hand(matched_card))
        self.recap(env)
        self.change_cur_player(env, 1, 0)


class DrawCardRule(BartokRule):
    def __init__(self):
        self.name = BartokRuleEnum.DRAWCARD
        self.draw2_rule = Draw2Rule()
        self.place_draw2_rule = PlayDraw2Rule()
        self.skip_rule = PlaySkipRule()
        self.reverse_rule = PlayReverseRule()
        self.place_match_rule = PlayMatchRule()

    def can_act(self, player, env):
        return (not self.draw2_rule.can_act(player, env)) and \
               (not self.place_draw2_rule.can_act(player, env)) and \
               (not self.skip_rule.can_act(player, env)) and \
               (not self.reverse_rule.can_act(player, env)) and \
               (not self.place_match_rule.can_act(player, env))

    def act(self, player, env):
        print("You cannot play any cards. Automatically adding one card to your hand.")
        self.add_to_hand_from_deck(player, env)
        self.change_cur_player(env, 1, 0)


BARTOK_RULES = [Draw2Rule, PlayDraw2Rule,
                PlaySkipRule, PlayReverseRule,
                PlayMatchRule, DrawCardRule]
