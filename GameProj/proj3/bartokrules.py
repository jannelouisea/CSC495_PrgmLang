from rule import Rule
from enums import BartokRuleEnum
from gamerules import GameRules
from env import BartokEnv
from common import prompt_input


class BartokRules(GameRules):
    def __init__(self, player):
        super().__init__(player)
        self.rules = [Draw2Rule(player), PlaceCardRule(player), DrawCardRule(player)]


class BartokRule(Rule):
    def __init__(self, player):
        super().__init__(player)

    def draw2_count(self):
        return self.env[BartokEnv.draw2_effect] * 2

    def reset_draw2_effect(self):
        self.env[BartokEnv.draw2] = False
        self.env[BartokEnv.draw2_effect] = 0

    def inc_draw2_effect(self):
        self.env[BartokEnv.draw2] = True
        self.env[BartokEnv.draw2_effect] += 1

    def check_deck(self):
        deck = self.env[BartokEnv.deck]
        center = self.env[BartokEnv.center]

        if deck.is_empty():
            add_count = center.num_cards() - 1
            for i in range(0, add_count):
                deck.put(center.take_bottom(), False)

    # TODO: Put into rule if other games need this functionality
    # TODO: Abstract check_deck() ?
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


class Draw2Rule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.DRAW2

    def can_act(self):
        can_act = False
        has_draw2_card = False

        for card in self.player.hand:
            if card.matches_rank('2'):
                has_draw2_card = True
        if self.env[BartokEnv.draw2] and not has_draw2_card:  # mustDraw2 is only True when a player has started
            can_act = True  # the Draw 2 effect or added to the effect
        return can_act  # mustDraw2 is set back to false when a player has drawn the
        # the cards

    def act(self):
        draw_count = self.draw2_count()
        print(f"Your only option is to draw {draw_count} cards.")
        print(f"Automatically adding {draw_count} cards to your hand.")
        self.add_to_hand_from_deck(draw_count)

        self.reset_draw2_effect()
        self.change_curr_player(1, 0)


class PlaceCardRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.PLACECARD
        self.place_msg = '** can play **'
        self.place_draw2_msg = '** draw 2 **'

    def place_cond(self, card):
        center_card = self.env[BartokEnv.center].look_top()
        return card.matches_rank(center_card.rank) or card.matches_suit(center_card.suit) or card.matches_rank('2')

    @staticmethod
    def place_draw2_cond(card):
        return card.matches_rank('2')

    @staticmethod
    def confirm_draw2_cond(choice):
        return int(choice) == 0 or int(choice) == 1

    def can_act(self):
        center_card = self.env[BartokEnv.center].look_top()
        can_place = False
        for card in self.player.hand:
            if card.matches_rank(center_card.rank) \
                    or card.matches_suit(center_card.suit) \
                    or card.matches_rank('2'):
                can_place = True
                break
        return can_place

    def user_place_card(self, possible_cards):
        def choose_card_cond(card_idx):
            return int(card_idx) in possible_cards

        player = self.player
        center = self.env[BartokEnv.center]
        self.player.show_hand([(self.place_cond, self.place_msg), (self.place_draw2_cond, self.place_draw2_msg)])

        chosen_card = -1
        if len(possible_cards) == 1:  # there's only one card the player can put down
            chosen_card = possible_cards.pop()
            card = player.hand[chosen_card]
            print(f"{card} is the only card you can play. Playing it automatically.")
        else:
            choose_card_prompt = 'Enter the INDEX of the card you would like to place.\n> '
            choose_card_err = f"You cannot place that card \nPossible card indexes to play {possible_cards}"
            chosen_card = int(prompt_input(choose_card_prompt, choose_card_cond, None, choose_card_err, None))

        center.put(player.rmv_from_hand(chosen_card))
        center_card = center.look_top()
        print(f"Player {self.player.pos} placed {center_card} in Center")
        return center_card

    def act(self):
        # This is true only when another player has started the Draw 2 effect
        # and the current player has the option to add to that effect
        if self.env[BartokEnv.draw2]:
            confirm_draw2_prompt = "Draw 2 effect started. " \
                                   "Add Draw 2 card to increase effect for next person?\n0 - No\n1 - Yes\n> "
            confirm_draw2_err = "Invalid input."
            choice = int(prompt_input(confirm_draw2_prompt, self.confirm_draw2_cond, None, confirm_draw2_err, None))

            if choice == 0:
                print("Wow, you're a pretty nice person. The next player should buy you a drink.")

                self.add_to_hand_from_deck(self.draw2_count())
                self.reset_draw2_effect()
            # Player chose Yes
            else:
                self.user_place_card(self.player.cards_meet_criteria([self.place_draw2_cond]))
                self.env[BartokEnv.draw2_effect] += 1
        else:
            center_card = self.user_place_card(self.player.cards_meet_criteria([self.place_cond]))
            if center_card.matches_rank('2'):
                self.inc_draw2_effect()
            else:
                self.reset_draw2_effect()

        self.change_curr_player(1, 0)


class DrawCardRule(BartokRule):
    def __init__(self, player):
        super().__init__(player)
        self.name = BartokRuleEnum.DRAWCARD

    def can_act(self):
        return True

    def act(self):
        print("Your only option is to draw from the deck")
        print("Automatically adding one card to your hand.")
        self.add_to_hand_from_deck()
        self.change_curr_player(1, 0)
