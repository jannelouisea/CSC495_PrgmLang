import sys
from spoons import Spoons
from bartok import Bartok
from enums import Game

games = [Bartok(Game.BARTOK), Spoons(Game.SPOONS)]


def game_choice_msg():
    msg = 'Which game would you like to play?\n'
    for idx, game_inst in enumerate(games):
        msg += f'{idx} - {game_inst.name}\n'
    msg += '> '
    return msg


if __name__ == '__main__':
    print("Let's Play! :D")

    game_choice = int(input(game_choice_msg()))
    if game_choice >= len(games) or game_choice < 0:
        sys.exit("Incorrect value submitted. Canceling game.")

    game = games[game_choice]
    game.set_up()
    game.play()
