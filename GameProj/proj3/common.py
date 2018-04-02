import sys


def prompt_input(prompt, input_cond, success_msg, error_msg, error_func):
    satisfied = False
    user_input = None

    while not satisfied:
        user_input = input(prompt)
        if input_cond(user_input):
            satisfied = True
            if success_msg:
                print(success_msg)
        else:
            if error_msg:
                print(error_msg, file=sys.stderr)
            if error_func:
                error_func()

    return user_input
