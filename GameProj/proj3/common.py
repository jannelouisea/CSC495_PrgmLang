import sys


def prompt_input(prompt, input_cond, error_msg, success_msg=None, error_func=None):
    satisfied = False
    user_input = None

    while not satisfied:
        input_valid = False
        try:
            user_input = int(input(prompt))
            input_valid = True
        except ValueError:
            err_color = '\033[91m'
            end_color = '\033[0m'
            print(f"{err_color}ERROR: Invalid input type. Input must be an integer.{end_color}")

        if input_valid:
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
