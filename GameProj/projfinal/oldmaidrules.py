from rule import Rule
from enums import OldmaidRuleEnum


# ------------------------------------------------------------------------------------------------- #
# The parent class for each rule in Spoons.                                                         #
# The class contains Spoons related functions used in the rule.                              #
# ------------------------------------------------------------------------------------------------- #
class OldmaidRule(Rule):
    def __init__(self, env):
        super().__init__(env)


    @staticmethod
    def add_to_hand_from_pass_pile(player, pass_pile):
        player.add_to_hand(pass_pile.take())

    def matching_card_cond(self, player):
        restart = True
        while restart:
            restart = False
            for index in range(0, len(player.hand)):
                for index2 in range(index + 1, len(player.hand)):
                    if player.hand[index].matches_rank(player.hand[index2].rank):
                        del(player.hand[index2])
                        del(player.hand[index])
                        restart = True
                        break
                else:
                    continue
                break


# ------------------------------------------------------------------------------------------------- #
# The dealer                                                                                        #
# ------------------------------------------------------------------------------------------------- #
class BeginRule(OldmaidRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = OldmaidRuleEnum.BEGIN

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self, player):
        return self.env.cur_player_pos == 0 and self.env.flag == False

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self, player):
        added_card = self.env.deck.take_top()
        player.add_to_hand(added_card)
        self.env.flag = True
        # check for matching cards
        self.matching_card_cond(player)
        print("After removing matching cards:")
        player.show_hand()
        self.change_cur_player(1, 0)


# ------------------------------------------------------------------------------------------------- #
# The dealer                                                                                        #
# ------------------------------------------------------------------------------------------------- #
class DealerRule(OldmaidRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = OldmaidRuleEnum.DEALER

    def can_act(self, player):
        return self.env.cur_player_pos == 0 and self.env.flag == True

    def act(self, player):
        # cards to pick from
        cards_available = len(self.env.players[1].hand)
        cards = player.cards_meet_cond()
        discard = self.oldmaid_choose_card(cards, cards_available)
        #remove from other player's hand
        #add to dealer's hand
        print("You chose card: {}".format(self.env.players[1].hand[discard]))
        player.hand.append(self.env.players[1].rmv_from_hand(discard))
        # check for matching cards
        self.matching_card_cond(player)
        print("After removing matching cards:")
        player.show_hand()
        self.change_cur_player(1, 0)


class PassRule(OldmaidRule):
    def __init__(self, env):
        super().__init__(env)
        self.name = OldmaidRuleEnum.PASS

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self, player):
        return self.env.cur_player_pos == 1 and self.env.flag == True

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def act(self, player):
        cards_available = len(self.env.players[0].hand)
        cards = player.cards_meet_cond()
        discard = self.oldmaid_choose_card(cards, cards_available)
        # remove from other dealer's hand
        # add to other player's hand
        print("You chose card: {}".format(self.env.players[0].hand[discard]))
        player.hand.append(self.env.players[0].rmv_from_hand(discard))
        # check for matching cards
        self.matching_card_cond(player)
        print("After removing matching cards:")
        player.show_hand()
        self.change_cur_player(1, 0)



OLDMAID_RULES = [BeginRule, DealerRule, PassRule]
