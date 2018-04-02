from game import Game
from env import BartokEnv
from pile import Pile
from common import prompt_input

BARTOK_SUMMARY = '''
Bartok Requirements:
 A standard deck of cards (without Jokers)
 2 to 5 players
 5 to 7 card to start
Game Play:
 The first player to get rid of all cards from their hand wins.
 Each player is initially dealt five to seven cards.
 Players place cards in the center Pile.
 After dealing cards to each player, the top card from the deck is placed
 face up in the center.
 Each player must place a card matching the suit or rank of the 
 top card of the center pile.
 If a player cannot place a card, they must draw one card from the deck (This is done automatically).
 If the top card is a Draw 2 card (i.e. card with rank 2) and the player cannot
 add another Draw 2 card, they must draw n cards from the deck where n equals the number
 of cumulative Draw 2 cards * 2 (This is also done automatically).
'''


class Bartok(Game):

    def __init__(self, game):
        super(Bartok, self).__init__(game)
        self.min_players = 2
        self.max_players = 5
        self.start_card_min = 5
        self.start_card_max = 7
        self.name = 'Bartok'
        self.env[BartokEnv.center] = Pile()
        self.env[BartokEnv.draw2] = False
        self.env[BartokEnv.draw2_effect] = 0

    def num_cards_cond(self, num_cards):
        return not(int(num_cards) < self.start_card_min or int(num_cards) > self.start_card_max)

    def player_trans_valid(self, player_pos):
        print(f"player_pos: {player_pos}")
        print(f"cur_player_pos: {self.env[BartokEnv.cur_player_pos]}")
        return int(player_pos) == self.env[BartokEnv.cur_player_pos]

    def set_up(self):
        print("Setting up Bartok")
        self.set_norm_deck()
        num_players = self.ask_num_players(self.min_players, self.max_players)

        num_cards_prompt = f'How many cards should each player start with? ' \
                           f'Must be between {self.start_card_min} or {self.start_card_max} cards.\n> '
        num_cards_err = 'ERROR: Incorrect number of start cards.'
        num_cards = int(prompt_input(num_cards_prompt, self.num_cards_cond, None, num_cards_err, None))

        self.init_players(num_players, num_cards)
        self.env[BartokEnv.center].put(self.env[BartokEnv.deck].take_top())

    def show_center_top_card(self):
        top_card = self.env[BartokEnv.center].look_top()
        print("=============================")
        print(f"Center Card: {top_card}")
        print("=============================")

    def let_curr_player_play(self):
        cur_player = self.cur_player()
        print(f"Player {cur_player.pos} Turn")
        print("-----------------------------")
        cur_player.weigh_actions()
        cur_player.act()

    def transition_to_next_player(self):
        rec = self.env[BartokEnv.rec_player_pos]
        cur = self.env[BartokEnv.cur_player_pos]
        print("-----------------------------")
        player_trans_prompt = f"Player {rec} your turn is over.\n" \
                              f"When Player {cur} is ready, enter your number ({cur}).\n> "
        player_trans_err = f"ERROR: The next player should be Player {cur}. " \
                           f"Please enter {cur} to proceed."
        prompt_input(player_trans_prompt, self.player_trans_valid, None, player_trans_err, None)

    def play(self):
        print("Let's play Bartok!")
        print(BARTOK_SUMMARY)

        while self.env[BartokEnv.winner_pos] < 0:
            self.show_center_top_card()
            self.let_curr_player_play()

            if self.env[BartokEnv.winner_pos] >= 0:
                print(f"Player {self.env[BartokEnv.winner_pos]} has won the game!")
                break

            self.transition_to_next_player()

    def det_winner(self):
        for player in self.env[BartokEnv.players]:
            if player.hand_size() == 0:
                self.env[BartokEnv.winner_pos] = player.pos
                break
