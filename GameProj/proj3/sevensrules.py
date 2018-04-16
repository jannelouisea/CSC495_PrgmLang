from rule import Rule
from enums import SevensRuleEnum, Suit
from card import Card
from cardpatterns import adjacent_high, adjacent_low, sort_cards, unavailable


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class SevensRules(GameRules):
    def __init__(self, player):
        super().__init__(player)
        self.rules = [PlayStartCardRule(player), PlayStartLayoutCardRule(player),
                      PlayAdjacentCardRule(player), KnockRule(player)]
        self.rules_map = {i: val for i, val in enumerate(self.rules)}


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class SevensRule(Rule):
    def __init__(self, player):
        super().__init__(player)
        self.table = {
            Suit.SPADES: self.env[SevensEnv.spades_layout],
            Suit.DIAMONDS: self.env[SevensEnv.diamonds_layout],
            Suit.CLUBS: self.env[SevensEnv.clubs_layout],
            Suit.HEARTS: self.env[SevensEnv.hearts_layout],
        }

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def put_card_on_table(self, card):
        print(f"Player {self.player.pos} placed {self.player.hand[card]} on the table.")
        layout = self.table[self.player.hand[card].suit]
        layout.put(self.player.rmv_from_hand(card))
        layout.sort_cards(sort_cards)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class PlayStartCardRule(SevensRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = SevensRuleEnum.PLAYSTARTCARD

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def start_card_cond(card):
        start_card = Card("7", Suit.DIAMONDS, 7)
        return card.matches_card(start_card)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return self.player.has_card_meet_cond(self.start_card_cond)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        print(f"Player {self.player.pos} has starting card.")
        start_card = self.player.cards_meet_cond(self.start_card_cond)[0]
        self.put_card_on_table(start_card)
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class PlayStartLayoutCardRule(SevensRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = SevensRuleEnum.PLAYSTARTLAYOUTCARD
        self.play_start_card_rule = PlayStartCardRule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    @staticmethod
    def start_layout_card_cond(card):
        return card.matches_rank('7')

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.play_start_card_rule.can_act()) and \
               self.player.has_card_meet_cond(self.start_layout_card_cond)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        print(f"Player {self.player.pos} has starting layout card.")
        start_layout_cards = self.player.cards_meet_cond(self.start_layout_card_cond)
        start_layout_card = start_layout_cards[0] if len(start_layout_cards) == 1 \
                            else self.user_choose_card(start_layout_cards, "start layout")
        self.put_card_on_table(start_layout_card)
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class PlayAdjacentCardRule(SevensRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = SevensRuleEnum.PLAYADJACENTCARD
        self.play_start_card_rule = PlayStartCardRule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def det_adjacent_cards(self):
        adjacent_cards = {
            Suit.SPADES: [],
            Suit.DIAMONDS: [],
            Suit.CLUBS: [],
            Suit.HEARTS: [],
        }

        for suit, layout in self.table.items():
            if not layout.is_empty() and layout.num_cards() < 13:
                if layout.num_cards() == 1:
                    adjacent_cards[suit].append('6')
                    adjacent_cards[suit].append('8')
                else:
                    layout.sort_cards(sort_cards)
                    top_card = layout.look_top()
                    adjacent_high_card = adjacent_high(top_card.rank)
                    bottom_card = layout.look_bottom()
                    adjacent_low_card = adjacent_low(bottom_card.rank)

                    if not (adjacent_high_card == unavailable):
                        adjacent_cards[suit].append(adjacent_high_card)
                    if not (adjacent_low_card == unavailable):
                        adjacent_cards[suit].append(adjacent_low_card)

        return adjacent_cards

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def adjacent_card_cond(self, card):
        adjacent_cards = self.det_adjacent_cards()
        layout = adjacent_cards[card.suit]
        return card.rank in layout

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.play_start_card_rule.can_act()) and \
               self.player.has_card_meet_cond(self.adjacent_card_cond)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        print(f"Player {self.player.pos} has adjacent card.")
        adjacent_cards = self.player.cards_meet_cond(self.adjacent_card_cond)
        adjacent_card = adjacent_cards[0] if len(adjacent_cards) == 1 \
                        else self.user_choose_card(adjacent_cards, "adjacent")
        self.put_card_on_table(adjacent_card)
        self.change_curr_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class KnockRule(SevensRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = SevensRuleEnum.KNOCK
        self.play_start_card_rule = PlayStartCardRule(player)
        self.play_start_layout_card_rule = PlayStartLayoutCardRule(player)
        self.play_adjacent_card_rule = PlayAdjacentCardRule(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (not self.play_start_card_rule.can_act()) and \
               (not self.play_start_layout_card_rule.can_act()) and \
               (not self.play_adjacent_card_rule.can_act())

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        print(f"Player {self.player.pos} knocked.")
        self.change_curr_player(1, 0)
