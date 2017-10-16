import random
name = 'randombot'
class RPSBot(object):
    name = name
    def __init__(self):
        self.moves = ['R','P','S']
    def get_hint(self, opp_moves, my_moves):
        return random.choice(self.moves)
    def get_move(self, opp_moves, my_moves, opp_hint, my_hint):
        return random.choice(self.moves)