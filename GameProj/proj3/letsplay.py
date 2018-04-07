import sys
from spoons import Spoons
from bartok import Bartok
from enums import Game
from common import prompt_input

games = [Bartok(Game.BARTOK), Spoons(Game.SPOONS)]


def game_choice_prompt():
    msg = 'Which game would you like to play?\n'
    for idx, game_inst in enumerate(games):
        msg += f'{idx} - {game_inst.name}\n'
    msg += '> '
    return msg


def game_choice_cond(choice):
    return int(choice) < len(games) and int(choice) >= 0


if __name__ == '__main__':
    print("=================================")
    print("Let's Play! :D")
    print('---------------------------------')

    game_choice_err = "Invalid Input."
    game_choice = int(prompt_input(game_choice_prompt(), game_choice_cond, game_choice_err))

    game = games[game_choice]
    game.set_up()
    game.play()
