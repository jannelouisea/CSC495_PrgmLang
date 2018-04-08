

# ------------------------------------------------------------------------------------------------- #
#                                                                                                   #
# ------------------------------------------------------------------------------------------------- #
def prompt_input(prompt, input_cond, error_msg, success_msg=None, error_func=None):
    error_color = '\033[91m'
    end_color = '\033[0m'
    satisfied = False
    user_input = None

    while not satisfied:
        input_valid = False
        try:
            user_input = int(input(prompt))
            input_valid = True
        except ValueError:
            print(f"{error_color}ERROR: Invalid input type. Input must be an integer.{end_color}")

        if input_valid:
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
