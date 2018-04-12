from rule import Rule
from enums import BartokRuleEnum
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
        self.rules = [PassRule(player)]
        self.rules_map = {i: val for i, val in enumerate(self.rules)}


# ------------------------------------------------------------------------------------------------- #
# The parent class for each rule in Spoons.                                                         #
# The class contains Spoons related functions used in the rule.                              #
# ------------------------------------------------------------------------------------------------- #
class SpoonsRule(Rule):
    def __init__(self, player):
        super().__init__(player)


    # ------------------------------------------------------------------------------------------------- #
    # Checks if the current deck is empty and refills the deck from the center pile if the deck is      #
    # empty.                                                                                            #
    # ------------------------------------------------------------------------------------------------- #
    def check_deck(self):
        deck = self.env[SpoonsEnv.deck]
        center = self.env[SpoonsEnv.center]

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
# Spoons' only rule                                                                            #
# ------------------------------------------------------------------------------------------------- #
class PassRule(SpoonsRule):
    def __init__(self, player):
        super().__init__(player)
        self.tempPile = []

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def add_to_hand_from_tempPile(self, tempPile):
        self.player.add_to_hand(tempPile.pop())

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        return True

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        if self.player.pos == self.env[Env.num_players] - 1:
            self.add_to_hand_from_tempPile(self.tempPile)
            #discard card
        elif self.player.pos == 0:
            self.add_to_hand_from_deck()
            #add card to temp pile
        else:
            self.add_to_hand_from_tempPile(self.tempPile)
            #give card to next player
        self.change_curr_player(1, 0)
