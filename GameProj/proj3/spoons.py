from game import Game
from env import SpoonsEnv
from cardpatterns import any_four_of_a_kind
from pile import Pile

SPOONS_SUMMARY = '''
Let's play Spoons!
Spoons Requirements:
A standard deck of cards (without Jokers)
3 to 13 players
Game Play:
The first person with four matching cards wins.
Each player is dealt four cards.
The dealer (Player 1) takes a card off the top of the deck to have five cards in their hand
They remove one card and pass it to the left.
Each person discards to the person on the left.
If you are the last player, you discard to the trash pile.
If the deck ever runs out, the trash pile is shuffled and replaces the deck.
If you have four matching cards in your hand, you must discard the fifth non-matching card to win the game.
'''


class Spoons(Game):

    def __init__(self, game):
        super(Spoons, self).__init__(game)
        self.name = 'Spoons'
        self.min_players = 3
        self.max_players = 13
        self.init_hand_size = 4
        self.env[SpoonsEnv.trash] = Pile()
        self.env[SpoonsEnv.end_player] = 0

    # ------------------------------------------------------------------------------------------------- #
    #                                                                                                   #
    # ------------------------------------------------------------------------------------------------- #
    def winning_cond(self, player):
        return any_four_of_a_kind(self, player)

    @staticmethod
    def num_player_cond(num_players):
        return not(int(num_players) < 3 or int(num_players) > 13)

    def set_up(self):
        print("Setting up Spoons...")
        self.set_norm_deck()
        self.env.num_players = self.ask_num_players(self.min_players, self.max_players)
        self.init_players(self.init_hand_size)
        self.env.end_player = self.env.num_players - 1

    def play(self):
        print(SPOONS_SUMMARY)
        while self.env[SpoonsEnv.winner_pos] < 0:
            self.let_cur_player_play()
            self.check_winner(self.winning_cond)
        '''
        num_players = self.env.num_players
        temp = []  # should always have only one card
        player = self.env['players'][0]
        while any_four_of_a_kind(self, player) == False:
            for i in range(num_players):
                player = self.env['players'][i]
                if i == num_players - 1:
                    #adds card that player gave
                    player.addToHand(temp.pop())
                    print("\nPlayer {} these are your cards: ".format(i + 1))
                    #adds card from hand to trash pile
                    player.reflect()
                    num = int(input("Please input the card number to discard (1-5) \n"))
                    if num < 1 | num > 5:
                        num = int(input("Please input a number between 1 and 5 \n"))
                    self.env['trash'].put(player.hand.pop(num - 1))
                    if any_four_of_a_kind(self, player) == True:
                        break
                    nextPlayer = int(input("Player {} your turn is over. When Player {} is ready for their turn enter their number. \n".format(i + 1, 1)))
                    if nextPlayer != 1:
                        int(input("The next player should be Player {}. Please enter {} to proceed.\n".format(1, 1)))
                elif i == 0:
                    #adds new card from deck
                    if len(self.env['deck'].cards) == 0:
                        self.env['deck'] = self.env['trash'].shuffle()
                    player.addToHand(self.env['deck'].takeTop())
                    print("\nA card has been drawn from the top of the deck and added to your hand. ")
                    print("Player 1 these are your cards: ")
                    player.reflect()
                    num = int(input("Please input the card number to discard (1-5) \n"))
                    if num < 1 | num > 5:
                        num = int(input("Please input a number between 1 and 5 \n"))
                    #gives card to next player
                    temp.append(player.hand.pop(num-1))
                    if any_four_of_a_kind(self, player) == True:
                        break
                    nextPlayer = int(input(
                        "Player {} your turn is over. When Player {} is ready for their turn enter their number. \n".format(
                            i + 1, i + 2)))
                    if nextPlayer != (i + 2):
                        int(input("The next player should be Player {}. Please enter {} to proceed.\n".format(i + 2, i + 2)))
                else:
                    #adds card that player gave
                    player.addToHand(temp.pop())
                    print("\nPlayer {} these are your cards: ".format(i + 1))
                    #gives card to next player
                    player.reflect()
                    num = int(input("Please input the card number to discard (1-5) \n"))
                    if num < 1 | num > 5:
                        num = int(input("Please input a number between 1 and 5 \n"))
                    temp.append(player.hand.pop(num-1))
                    if any_four_of_a_kind(self, player) == True:
                        break
                    nextPlayer = int(input(
                        "Player {} your turn is over. When Player {} is ready for their turn enter their number. \n".format(
                            i + 1, i + 2)))

                    if nextPlayer != (i + 2):
                        int(input("The next player should be Player {}. Please enter {} to proceed.\n".format(i + 2, i + 2)))
        print("Player {} these are your cards: ".format(i + 1))
        player.reflect()
        print('Player {} has won'.format(i + 1))
        '''
        print('In the works')

