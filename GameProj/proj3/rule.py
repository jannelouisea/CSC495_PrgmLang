from env import Env
from common import prompt_input


# ------------------------------------------------------------------------------------------------- #
# Parent class for any rule in a game.                                                              #
# The class contains common functions used for any rule in any game.                                #
#                                                                                                   #
# :attribute player: A player instance.                                                             #
# :attribute env: The shared environment between all objects in a game.                             #
# ------------------------------------------------------------------------------------------------- #
class Rule:

    def __init__(self, player):
        self.player = player
        self.env = player.env

    # ------------------------------------------------------------------------------------------------- #
    # Changes the environment's recent and current player positions.                                    #
    # The recent player position is changed to the current player's position.                           #
    # The current player position is determined by the next player function.                            #
    #                                                                                                   #
    # :param jump_size: Number of players to go to.                                                     #
    # :param skips: Number of players to skip.                                                          #
    # ------------------------------------------------------------------------------------------------- #
    def change_curr_player(self, jump_size, skips):
        self.env[Env.rec_player_pos] = self.env[Env.cur_player_pos]
        self.env[Env.cur_player_pos] = self.next_player(jump_size, skips)

    # ------------------------------------------------------------------------------------------------- #
    # Determines the next player in a circle of players.                                                #
    #                                                                                                   #
    # Algorithm                                                                                         #
    # next player = (current player position) +                                                         #
    #               (direction * (jump size * (skips + 1)) % number of players)                         #
    #                                                                                                   #
    # If the next player is outside the valid range of player positions [0 - (number of players - 1)],  #
    # the number of players is added or subtracted with respect to                                      #
    # the direction (clockwise or counter-clockwise).                                                   #
    #                                                                                                   #
    # :param player: The current player.                                                                #
    # :param jump_size: Number of players to go to.                                                     #
    # :param skips: Number of players to skip.                                                          #
    # :return: The index of the next player.                                                            #
    # ------------------------------------------------------------------------------------------------- #
    def next_player(self, jump_size, skips):
        cur_player_pos = self.env[Env.cur_player_pos]
        direction = self.env[Env.direction]
        num_players = self.env[Env.num_players]
        last_idx = num_players - 1

        next_player = cur_player_pos + (direction * ((jump_size * (skips + 1)) % num_players))

        if next_player < 0 or next_player > last_idx:
            next_player -= direction * num_players

        return next_player

    # ------------------------------------------------------------------------------------------------- #
    # Prompts the user to choose a card from the valid list of cards.                                   #
    #                                                                                                   #
    # :param valid_cards: A list of valid cards indices from the player's hand.                         #
    # :param card_type: The type of card each card associates with; used in the prompt.                 #
    # ------------------------------------------------------------------------------------------------- #
    def user_choose_card(self, valid_cards, card_type=''):
        def valid_card(idx):
            return int(idx) in valid_cards

        choose_card_prompt = f"Enter the index of the {card_type} card would you like to play.\nIndex - Card\n"
        for card in valid_cards:
            choose_card_prompt += f"{card} - {self.player.hand[card]}\n"
        choose_card_prompt += "> "
        choose_card_err = "ERROR: Invalid index."
        return int(prompt_input(choose_card_prompt, valid_card, choose_card_err))

    # ------------------------------------------------------------------------------------------------- #
    # An interface for each rule's can_act function.                                                    #
    # The can_act function is used to determine if the player can act on the rule based on the player's #
    # state and the state of the environment.                                                           #
    # When implemented, it should return a boolean value.                                               #
    # ------------------------------------------------------------------------------------------------- #
    def can_act(self):
        pass

    # ------------------------------------------------------------------------------------------------- #
    # An interface for each rule's act function.                                                        #
    # The act function is called only when the rule's can_act function returns true and the user        #
    # selects the rule to act upon.                                                                     #
    # ------------------------------------------------------------------------------------------------- #
    def act(self):
        pass
