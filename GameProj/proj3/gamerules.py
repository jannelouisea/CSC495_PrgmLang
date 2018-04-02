from thing import Thing

class GameRules(Thing):
    def __init__(self, player):
        self.player = player
        self.env = player.env
