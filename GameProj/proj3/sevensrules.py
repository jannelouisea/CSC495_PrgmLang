from rule import Rule
from enums import SevensRuleEnum, Suit
from cardpatterns import adjacent_high, adjacent_low, sort_cards, unavailable


class SevensRule(Rule):
    def __init__(self, env):
        super().__init__(env)
        self.table = {
            Suit.SPADES: self.env.spades_layout,
            Suit.DIAMONDS: self.env.diamonds_layout,
            Suit.CLUBS: self.env.clubs_layout,
            Suit.HEARTS: self.env.hearts_layout,
        }

    def put_card_on_table(self, player, card):
        print(f"Player {player.pos} placed {player.hand[card]} on the table.")
        layout = self.table[player.hand[card].suit]
        layout.put(player.rmv_from_hand(card))
        layout.sort_cards(sort_cards)


class PlayStartCardRule(SevensRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = SevensRuleEnum.PLAYSTARTCARD

    @staticmethod
    def start_card_cond(card):
        return card.matches_rank('7') and card.matches_suit(Suit.DIAMONDS)

    def can_act(self, player):
        return player.has_card_meet_cond(self.start_card_cond)

    def act(self, player):
        print(f"Player {player.pos} has starting card.")
        start_card = player.cards_meet_cond(self.start_card_cond)[0]
        self.put_card_on_table(player, start_card)
        self.change_cur_player(1, 0)


class PlayStartLayoutCardRule(SevensRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = SevensRuleEnum.PLAYSTARTLAYOUTCARD
        self.play_start_card_rule = PlayStartCardRule(env)

    @staticmethod
    def start_layout_card_cond(card):
        return card.matches_rank('7')

    def can_act(self, player):
        return (not self.play_start_card_rule.can_act(player)) and \
               player.has_card_meet_cond(self.start_layout_card_cond)

    def act(self, player):
        print(f"Player {player.pos} has starting layout card.")
        start_layout_cards = player.cards_meet_cond(self.start_layout_card_cond)
        start_layout_card = start_layout_cards[0] if len(start_layout_cards) == 1 \
                            else self.user_choose_card(player, start_layout_cards, "start layout")
        self.put_card_on_table(player, start_layout_card)
        self.change_cur_player(1, 0)


class PlayAdjacentCardRule(SevensRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = SevensRuleEnum.PLAYADJACENTCARD
        self.play_start_card_rule = PlayStartCardRule(env)

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

    def adjacent_card_cond(self, card):
        adjacent_cards = self.det_adjacent_cards()
        layout = adjacent_cards[card.suit]
        return card.rank in layout

    def can_act(self, player):
        return (not self.play_start_card_rule.can_act(player)) and \
               player.has_card_meet_cond(self.adjacent_card_cond)

    def act(self, player):
        print(f"Player {player.pos} has adjacent card.")
        adjacent_cards = player.cards_meet_cond(self.adjacent_card_cond)
        adjacent_card = adjacent_cards[0] if len(adjacent_cards) == 1 \
                        else self.user_choose_card(player, adjacent_cards, "adjacent")
        self.put_card_on_table(player, adjacent_card)
        self.change_cur_player(1, 0)


class KnockRule(SevensRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = SevensRuleEnum.KNOCK
        self.play_start_card_rule = PlayStartCardRule(env)
        self.play_start_layout_card_rule = PlayStartLayoutCardRule(env)
        self.play_adjacent_card_rule = PlayAdjacentCardRule(env)

    def can_act(self, player):
        return (not self.play_start_card_rule.can_act(player)) and \
               (not self.play_start_layout_card_rule.can_act(player)) and \
               (not self.play_adjacent_card_rule.can_act(player))

    def act(self, player):
        print(f"Player {player.pos} knocked.")
        self.change_cur_player(1, 0)


SEVENS_RULES = [PlayStartCardRule, PlayStartLayoutCardRule, PlayAdjacentCardRule, KnockRule]
