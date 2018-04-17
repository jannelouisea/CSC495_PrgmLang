from thing import Thing
from common import *
from env import Env
from sys import exit, stderr


# Example card game configuration
# card_game = {
#    ENV: Env,
#    DECK_SIZE: 1,
#    DECK_W_JOKERS: False,
#    NUM_PLAYERS: 3,
#    START_HAND_SIZE: 5,
#    DIRECTION: 1
# }


class CardGame(Thing):

    def __init__(self, game_params):
        # Setting up the environment
        deck_size = game_params.get(DECK_SIZE, 1)
        deck_w_jokers = game_params.get(DECK_W_JOKERS, False)
        num_players = game_params.get(NUM_PLAYERS, 1)
        start_hand_size = game_params.get(START_HAND_SIZE, 0)
        direction = game_params.get(DIRECTION, 1)
        if not self.valid_env_params(deck_size, deck_w_jokers, num_players, start_hand_size, direction):
            self.warn_invalid_params('ERROR: Env params are invalid.')
            exit(500)
        self.env = game_params.get(ENV, Env)(deck_size, deck_w_jokers, num_players, start_hand_size, direction)

        # Setting the rules
        game_rules = {i: rule(self.env) for i, rule in enumerate(game_params.get(GAME_RULES, []))}
        self.establish_rules(game_rules)

        # setting the game play
        self.setup = game_params.get(SETUP, self.do_nothing)
        self.pre_player_turn = game_params.get(PRE_PLAYER_TURN, self.do_nothing)
        self.post_player_turn = game_params.get(POST_PLAYER_TURN, self.do_nothing)
        self.winning_cond = game_params.get(WINNING_COND, self.do_nothing)

    @staticmethod
    def do_nothing(env):
        pass

    def warn_invalid_params(self, msg):
        print(msg, file=stderr)

    def valid_env_params(self, deck_size, deck_w_jokers, num_players, start_hand_size, direction):
        valid_params = True

        if not (type(deck_size) == int and (1 <= deck_size <= 10)):
            self.warn_invalid_params('ERROR: DECK_SIZE must be a positive integer between 1 and 10.')
            valid_params = False

        if not type(deck_w_jokers) == bool:
            valid_params = False
            self.warn_invalid_params('ERROR: DECK_W_JOKERS must be True or False.')

        if not (type(num_players) == int and (1 <= num_players <= 10)):
            self.warn_invalid_params('ERROR: NUM_PLAYERS must be a positive integer between 1 and 10.')
            valid_params = False

        if start_hand_size != EQUAL_NUM_CARDS and (not type(start_hand_size) == int or start_hand_size < 1):
            self.warn_invalid_params('ERROR: START_HAND_SIZE must be a positive integer greater than 0 or EQUAL_NUM_CARDS.')
            valid_params = False
        else:
            if start_hand_size != EQUAL_NUM_CARDS:
                num_cards_in_deck = deck_size * 52 if not deck_w_jokers else deck_size * 54
                if (num_players * start_hand_size) > num_cards_in_deck:
                    self.warn_invalid_params('ERROR: START_HAND_SIZE is too big for the DECK_SIZE and NUM_PLAYERS provided.')
                    valid_params = False

        if not (direction == CLOCKWISE or direction == COUNTER_CLOCKWISE):
            self.warn_invalid_params('ERROR: DIRECTION must be either CLOCKWISE (1) or COUNTER_CLOCKWISE (-1).')
            valid_params = False

        return valid_params

    def establish_rules(self, game_rules):
        for player in self.env.players:
            player.game_rules = game_rules

    def play(self):
        self.setup(self.env)

        while not self.env.found_winner():
            self.pre_player_turn(self.env)
            self.exec_player_turn()
            self.post_player_turn(self.env)
            self.check_winner()
            self.transition_player()

    def exec_player_turn(self):
        player = self.env.get_cur_player()
        print(f"Player {player.pos} Turn")
        print("---------------------------------")
        player.show_hand()
        possible_actions = player.possible_actions()
        if len(possible_actions) == 1:
            player.act(possible_actions[0][0])
        else:
            valid_actions = list()
            act_prompt = "What would you like to do?\n"
            for i, action in possible_actions:
                valid_actions.append(i)
                act_prompt += f"{i} - {action}\n"
            act_prompt += "> "
            act_err = "ERROR: Invalid index."

            def valid_action(input_action):
                return int(input_action) in valid_actions

            desired_action = int(prompt_input(act_prompt, valid_action, act_err))
            player.act(desired_action)

    def transition_cond(self, player_pos):
        return int(player_pos) == self.env.cur_player_pos

    def transition_player(self):
        rec = self.env.rec_player_pos
        cur = self.env.cur_player_pos
        print("---------------------------------")
        transition_prompt = f"Player {rec} your turn is over.\n" \
                            f"When Player {cur} is ready, enter your number ({cur}).\n> "
        transition_err = f"ERROR: The next player should be Player {cur}. " \
                         f"Please enter {cur} to proceed."
        prompt_input(transition_prompt, self.transition_cond, transition_err)

    def check_winner(self):
        if self.winning_cond(self.env):
            self.end_game(self.env.winner_pos)

    @staticmethod
    def end_game(winner_pos):
        print("=================================")
        print("*********************************")
        print(f"   Player {winner_pos} has won the game!")
        print("*********************************")
        print("=================================")
        exit()
