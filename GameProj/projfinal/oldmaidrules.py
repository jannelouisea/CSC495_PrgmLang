from rule import Rule
from enums import OldmaidRuleEnum


# ------------------------------------------------------------------------------------------------- #
# The parent class for each rule in Spoons.                                                         #
# The class contains Spoons related functions used in the rule.                              #
# ------------------------------------------------------------------------------------------------- #
class OldmaidRule(Rule):
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


    @staticmethod
    def add_to_hand_from_pass_pile(player, pass_pile):
        player.add_to_hand(pass_pile.take())

    def matching_card_cond(self, player):
        restart = True
        while restart:
            restart = False
            for index in range(0, len(player.hand)):
                print("index {}".format(index))
                for index2 in range(index + 1, len(player.hand)):
                    print("index2 {} ".format(index2))
                    if player.hand[index].matches_rank(player.hand[index2].rank):
                        print("before")
                        print(player.hand)
                        del(player.hand[index2])
                        del(player.hand[index])
                        restart = True
                        print("after")
                        print(player.hand)
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
        cards_available = len(player[1].hand)
        discard = self.oldmaid_choose_card(player, cards_available)
        #remove from other player's hand
        #add to dealer's hand
        self.player.hand.put(player[1].rmv_from_hand(discard))
        # check for matching cards
        self.matching_card_cond(self.player.hand)

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
        discard = self.oldmaid_choose_card(player, cards_available)
        # remove from other dealer's hand
        # add to other player's hand
        self.player.hand.put(self.env.players[0].rmv_from_hand(discard))
        # check for matching cards
        self.matching_card_cond(self.player.hand)

        self.change_cur_player(1, 0)



OLDMAID_RULES = [BeginRule, DealerRule, PassRule]
