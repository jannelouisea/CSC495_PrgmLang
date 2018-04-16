from rule import Rule
from enums import SpoonsRuleEnum


# ------------------------------------------------------------------------------------------------- #
# The parent class for each rule in Spoons.                                                         #
# The class contains Spoons related functions used in the rule.                              #
# ------------------------------------------------------------------------------------------------- #
class SpoonsRule(Rule):
    def __init__(self, env):
        super().__init__(env)

    # ------------------------------------------------------------------------------------------------- #
    # Checks if the current deck is empty and refills the deck from the trash pile if the deck is      #
    # empty.                                                                                            #
    # ------------------------------------------------------------------------------------------------- #
    def check_deck(self):
        deck = self.env.deck
        trash = self.env.trash

        if deck.is_empty():
            add_count = trash.num_cards() - 1
            for i in range(0, add_count):
                deck.put(trash.take_bottom(), False)

    # ------------------------------------------------------------------------------------------------- #
    # Given n a number of cards, n cards are taken from the deck and added to the player's hand.        #
    #                                                                                                   #
    # :param num_cards: Number of cards, default value is 1.                                            #
    # :param show: Boolean value to determine if the cards added are shown on the screen, default       #
    #               value set to True.                                                                  #
    # ------------------------------------------------------------------------------------------------- #
    def add_to_hand_from_deck(self, player, num_cards=1, show=True):
        added = list()
        self.check_deck()
        for i in range(num_cards):
            added_card = self.env.deck.take_top()
            player.add_to_hand(added_card)
            added.append(added_card)
            self.check_deck()
        if show:
            msg = "Added to hand:"
            for card in added:
                msg += f" {card}"
            print(msg)
        return added

    @staticmethod
    def add_to_hand_from_pass_pile(player, pass_pile):
        player.add_to_hand(pass_pile.take())


# ------------------------------------------------------------------------------------------------- #
# The dealer                                                                                        #
# ------------------------------------------------------------------------------------------------- #
class DealerRule(SpoonsRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = SpoonsRuleEnum.DEALER

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self, player):
        return self.env.cur_player_pos == 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self, player):
        self.add_to_hand_from_deck(player)
        # viewing cards
        cards = player.cards_meet_cond()
        discard = self.user_choose_card(player, cards)
        # give card to next player
        self.env.pass_pile.put(player.rmv_from_hand(discard))
        self.change_cur_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
# Any person between dealer and last player                                                         #
# ------------------------------------------------------------------------------------------------- #
class PassRule(SpoonsRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = SpoonsRuleEnum.PASS

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self, player):
        return self.env.cur_player_pos != 0 and self.env.cur_player_pos != self.env.end_player

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self, player):
        self.add_to_hand_from_pass_pile(player, self.env.pass_pile)
        # viewing cards
        cards = player.cards_meet_cond()
        discard = self.user_choose_card(player, cards)
        # give card to next player
        self.env.pass_pile.put(player.rmv_from_hand(discard))
        self.change_cur_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
# The last player                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class EndRule(SpoonsRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = SpoonsRuleEnum.END

    def can_act(self, player):
        return self.env.cur_player_pos == self.env.end_player

    def act(self, player):
        self.add_to_hand_from_pass_pile(player, self.env.pass_pile)
        # viewing cards
        cards = player.cards_meet_cond()
        discard = self.user_choose_card(player, cards)
        # give card to trash pile
        self.env.trash.put(player.rmv_from_hand(discard))
        self.change_cur_player(1, 0)


SPOONS_RULES = [DealerRule, PassRule, EndRule]
