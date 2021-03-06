# Environment Fields for Card Game Configuration
ENV = 'env'
DECK_SIZE = 'deck_size'
DECK_W_JOKERS = 'deck_w_jokers'
DECK_WO_QUEENS = 'deck_wo_queens'
NUM_PLAYERS = 'num_players'
START_HAND_SIZE = 'start_hand_size'
DIRECTION = 'direction'
GAME_RULES = 'game_rules'
SETUP = 'setup'
PRE_PLAYER_TURN = 'pre_player_turn'
POST_PLAYER_TURN = 'post_player_turn'
WIN_COND = 'win_cond'

# Field to notify to split cards equally between players
EQUAL_NUM_CARDS = -100

# Direction fields
CLOCKWISE = 1
COUNTER_CLOCKWISE = -1


# Win Conditions
# Note so far the only win condition is having an empty hand. When more
# win conditions arise then a new file can be made to hold common win conditions
def empty_hand_win_cond(env):
    for i, player in enumerate(env.players):
        if player.hand_size() == 0:
            env.winner_pos = i
            return True
    return False


# Common function used to ask user for input
def prompt_input(prompt, input_cond, error_msg, success_msg=None, error_func=None):
    error_color = '\033[91m'
    end_color = '\033[0m'
    satisfied = False
    user_input = None

    while not satisfied:
        input_type_valid = False
        try:
            user_input = int(input(prompt))
            input_type_valid = True
        except ValueError:
            print(f"{error_color}ERROR: Invalid input type. Input must be an integer.{end_color}")

        if input_type_valid:
            if input_cond(user_input):
                satisfied = True
                if success_msg:
                    print(success_msg)
            else:
                if error_msg:
                    print(f"{error_color}{error_msg}{end_color}")
                if error_func:
                    error_func()

    return user_input
