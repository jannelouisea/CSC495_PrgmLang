from rule import Rule
from enums import SpoonsRuleEnum
from gamerules import GameRules
from env import SpoonsEnv
from env import Env

# ------------------------------------------------------------------------------------------------- #
# The set of rules for Spoons.                                                                      #
#                                                                                                   #
# :attribute rules: A list of SpoonsRules.                                                          #
# :attribute rules_map: A mapping on SpoonsRules where the key is the position of the rule in       #
#                       rules, and the value is the rule.                                           #
# ------------------------------------------------------------------------------------------------- #
class SpoonsRules(GameRules):
    def __init__(self, player):
        super().__init__(player)
        self.rules = [DealerRule(player), PassRule(player), EndRule(player)]
        self.rules_map = {i: val for i, val in enumerate(self.rules)}


# ------------------------------------------------------------------------------------------------- #
# The parent class for each rule in Spoons.                                                         #
# The class contains Spoons related functions used in the rule.                              #
# ------------------------------------------------------------------------------------------------- #
class SpoonsRule(Rule):
    def __init__(self, player):
        super().__init__(player)


    # ------------------------------------------------------------------------------------------------- #
    # Checks if the current deck is empty and refills the deck from the trash pile if the deck is      #
    # empty.                                                                                            #
    # ------------------------------------------------------------------------------------------------- #
    def check_deck(self):
        deck = self.env[SpoonsEnv.deck]
        trash = self.env[SpoonsEnv.trash]

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
    def add_to_hand_from_deck(self, num_cards=1, show=True):
        added = list()
        self.check_deck()
        for i in range(num_cards):
            added_card = self.env[SpoonsEnv.deck].take_top()
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
    def add_to_hand_from_pass_pile(self, pass_pile):
        self.player.add_to_hand(pass_pile.pop())

# ------------------------------------------------------------------------------------------------- #
# The dealer                                                                                        #
# ------------------------------------------------------------------------------------------------- #
class DealerRule(SpoonsRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = SpoonsRuleEnum.DEALER

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (self.env[SpoonsEnv.cur_player_pos] == 0)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        self.add_to_hand_from_deck()
        # viewing cards
        cards = self.player.cards_in_hand()
        discard = self.spoons_choose(cards)
        # give card to next player
        self.env[SpoonsEnv.pass_pile].put(self.player.rmv_from_hand(discard))
        self.change_curr_player(1, 0)

# ------------------------------------------------------------------------------------------------- #
# Any person between dealer and last player                                                         #
# ------------------------------------------------------------------------------------------------- #
class PassRule(SpoonsRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = SpoonsRuleEnum.PASS

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (self.env[SpoonsEnv.cur_player_pos] != 0 or
                self.env[SpoonsEnv.cur_player_pos] != self.env[SpoonsEnv.end_player])

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        self.add_to_hand_from_pass_pile(self.env[SpoonsEnv.pass_pile])
        #viewing cards
        discard = self.spoons_choose(self.hand)
        # give card to next player
        self.env[SpoonsEnv.pass_pile].put(self.player.rmv_from_hand(discard))
        self.change_curr_player(1, 0)

# ------------------------------------------------------------------------------------------------- #
# The last player                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class EndRule(SpoonsRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = SpoonsRuleEnum.END

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return (self.env[SpoonsEnv.cur_player_pos] == self.env[SpoonsEnv.end_player])

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        self.add_to_hand_from_pass_pile(self.env[SpoonsEnv.pass_pile])
        #viewing cards
        discard = self.spoons_choose(self.hand)
        # give card to trash pile
        self.env[SpoonsEnv.trash].put(self.player.rmv_from_hand(discard))
        self.change_curr_player(1, 0)

