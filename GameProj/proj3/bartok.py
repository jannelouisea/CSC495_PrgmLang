from game import Game
from env import BartokEnv
from pile import Pile
from common import prompt_input

BARTOK_SUMMARY = '''
======================================================
                        Bartok
------------------------------------------------------
Bartok is a card game that uses a standard deck of
card without Jokers. The number of players can range
from 2 to 5 players and the number of cards each
player can start with range from 5 to 7 cards.

The objective of the game is to be the first player
to get rid of all their cards.

Special Cards in the Game:
Draw 2 card     - any card with rank 2
Skip Card       - any card with rank 7
Reverse Card    - any card with rank 8

Each player can do one the following moves on their
turn:
0 - Draw 2n Cards (n = draw2 effect)
    If the current player cannot add to the draw 2
    effect, then they must draw 2n cards from the
    deck, when n equals the number of previous players
    that consecutively placed a draw 2 card. 
    (This is done automatically)
           
1 - Play one Draw 2 Card (rank 2)

2 - Play one Skip Card (rank 7)

3 - Place one Reverse Card (rank 8)

4 - Play one Card w/ Matching Suit or Rank
    For this move, the player must play a card that
    matches the suit or rank to the top card in the
    center pile.
    
5 - Draw from Deck
    If the player cannot play any card, the player
    must draw one card from the deck.
    (This is done automatically)

If player can only play a single card of each type,
that card is automatically placed in the center. 

To transition between players, the next player has to
enter their position before proceeding.

Good Luck. Now let's play!
======================================================
'''


# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
class Bartok(Game):

    def __init__(self, game):
        super(Bartok, self).__init__(game)
        self.min_players = 2
        self.max_players = 5
        self.start_card_min = 5
        self.start_card_max = 7
        self.env[BartokEnv.center] = Pile()
        self.env[BartokEnv.draw2] = False
        self.env[BartokEnv.draw2_effect] = 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def winning_cond(self, player):
        return player.hand_size() == 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def num_cards_cond(self, num_cards):
        return not(int(num_cards) < self.start_card_min or int(num_cards) > self.start_card_max)

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def set_up(self):
        print("---------------------------------")
        print("Set Up")
        print("---------------------------------")
        self.set_norm_deck()
        num_players = self.ask_num_players(self.min_players, self.max_players)

        num_cards_prompt = f'How many cards should each player start with? ' \
                           f'Must be between {self.start_card_min} or {self.start_card_max} cards.\n> '
        num_cards_err = 'ERROR: Incorrect number of start cards.'
        num_cards = int(prompt_input(num_cards_prompt, self.num_cards_cond, num_cards_err))

        self.init_players(num_players, num_cards)
        self.env[BartokEnv.center].put(self.env[BartokEnv.deck].take_top())

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def show_center_top_card(self):
        top_card = self.env[BartokEnv.center].look_top()
        print("=================================")
        print(f"Center Card: {top_card}")
        print("=================================")

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def play(self):
        print(BARTOK_SUMMARY)

        while self.env[BartokEnv.winner_pos] < 0:
            self.show_center_top_card()
            self.let_cur_player_play()
            self.check_winner(self.winning_cond)
