from common import prompt_input
from thing import Thing


class Rule(Thing):

    def change_curr_player(self, env, jump_size, skips):
        env.rec_player_pos = env.cur_player_pos
        env.cur_player_pos = self.next_player(env, jump_size, skips)

    @staticmethod
    def next_player(env, jump_size, skips):
        cur_player_pos = env.cur_player_pos
        direction = env.direction
        num_players = env.num_players
        last_idx = num_players - 1

        next_player = cur_player_pos + (direction * ((jump_size * (skips + 1)) % num_players))

        if next_player < 0 or next_player > last_idx:
            next_player -= direction * num_players

        return next_player

    @staticmethod
    def user_choose_card(player, valid_cards, card_type=''):
        def valid_card(idx):
            return int(idx) in valid_cards

        choose_card_prompt = f"Enter the index of the {card_type} card would you like to play.\nIndex - Card\n"
        for card in valid_cards:
            choose_card_prompt += f"{card} - {player.hand[card]}\n"
        choose_card_prompt += "> "
        choose_card_err = "ERROR: Invalid index."
        return int(prompt_input(choose_card_prompt, valid_card, choose_card_err))

    def can_act(self, player, env):
        pass

    def act(self, player, env):
        pass
