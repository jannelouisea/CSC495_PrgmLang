from thing import Thing
from player import Player
from deck import Deck
from env import Env
from common import prompt_input
from card_patterns import sort_cards


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class Game(Thing):
    def __init__(self, game):
        self.game = game
        self.name = game.value
        self.env = {
            Env.deck: Deck(True),
            Env.players: [],
            Env.rec_player_pos: 0,
            Env.cur_player_pos: 0,
            Env.direction: 1,
            Env.winner_pos: -1
        }

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def transition_cond(self, player_pos):
        return int(player_pos) == self.env[Env.cur_player_pos]

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def set_norm_deck(self):
        self.env[Env.deck] = Deck()       # Deck without Jokers
        self.env[Env.deck].shuffle()

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def set_deck_w_jokers(self):
        self.env[Env.deck] = Deck(True)       # Deck without Jokers
        self.env[Env.deck].shuffle()

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def let_user_choose_deck(self):
        def deck_cond(x):
            return x == 0 or x == 1

        deck_prompt = 'Choose deck type.\n0 - Without Jokers\n1 - With Jokers'
        deck_err = 'Please enter 0 or 1.'
        prompt_input(deck_prompt, deck_cond, deck_err)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def ask_num_players(self, min_num, max_num):
        def num_player_cond(num_players):
            return not(int(num_players) < min_num or int(num_players) > max_num)

        num_player_prompt = f"How many players? Number must be between {min_num} and {max_num}.\n> "
        num_player_err = 'ERROR: Incorrect number of players.'
        num_players = int(prompt_input(num_player_prompt, num_player_cond, num_player_err))
        self.env[Env.num_players] = num_players
        return num_players

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def init_players(self, num_players, num_cards=0):
        for i in range(0, num_players):
            player = Player(self.env, i, self.game)
            for j in range(num_cards):
                player.add_to_hand(self.env[Env.deck].take_top())
            player.sort_hand(sort_cards)
            self.env[Env.players].append(player)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def init_players_w_eq_cards(self, num_players):
        players = self.env[Env.players]
        for i in range(0, num_players):
            players.append(Player(self.env, i, self.game))

        deck = self.env[Env.deck]
        num_cards = deck.num_cards()
        for i in range(0, num_cards):
            players[i % num_players].add_to_hand(deck.take_top())

        for player in players:
            player.sort_hand(sort_cards)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def cur_player(self):
        return self.env[Env.players][self.env[Env.cur_player_pos]]

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def let_cur_player_play(self):
        player = self.cur_player()
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
            def valid_action(action):
                return int(action) in valid_actions
            desired_action = int(prompt_input(act_prompt, valid_action, act_err))
            player.act(desired_action)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def transition_to_next_player(self):
        rec = self.env[Env.rec_player_pos]
        cur = self.env[Env.cur_player_pos]
        print("---------------------------------")
        transition_prompt = f"Player {rec} your turn is over.\n" \
                              f"When Player {cur} is ready, enter your number ({cur}).\n> "
        transition_err = f"ERROR: The next player should be Player {cur}. " \
                           f"Please enter {cur} to proceed."
        prompt_input(transition_prompt, self.transition_cond, transition_err)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def print_winner_msg(self, winner):
        print("=================================")
        print("*********************************")
        print(f"   Player {winner} has won the game!")
        print("*********************************")
        print("=================================")

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def check_winner(self, winning_cond):
        for player in self.env[Env.players]:
            if winning_cond(player):
                self.env[Env.winner_pos] = player.pos
                break
        if self.env[Env.winner_pos] >= 0:
            self.print_winner_msg(self.env[Env.winner_pos])
        else:
            self.transition_to_next_player()

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def play(self): pass

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def set_up(self): pass
