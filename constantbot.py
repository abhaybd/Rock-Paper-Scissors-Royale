# Constant RPS bot
name = 'constantbot'
import random
class RPSBot(object):
    name = name
    def __init__(self):
        self.move = random.choice(['R','P','S'])
    def get_hint(self, opp_moves, my_moves):
        return self.move
    def get_move(self, opp_moves, my_moves, opp_hint, my_hint):
        return self.move