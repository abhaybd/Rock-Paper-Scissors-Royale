# RPS Bot
name = 'truthyfalseybot'
import random
lose_against_map = {'S':'R', 'R':'P', 'P':'S'}
def is_trustworthy(moves, length):
    if len(moves) == 0:
        return False
    length = max(-length, -len(moves))
    history = [1 if move[0] == move[1] else 0 for move in moves[length:]]
    prob_honest = sum(history)/len(history)
    choice = random.uniform(0., 1.)
    if choice <= prob_honest:
        return True
    else:
        return False

class RPSBot(object):
    name = name
    def __init__(self):
        self.moves = ['R','P','S']
        self.length = 10
    def get_hint(self, opp_moves, my_moves):
        return random.choice(self.moves)
        
    def get_move(self, opp_moves, my_moves, opp_hint, my_hint):
        """
        if len(opp_moves) < self.length:
            return my_hint
        """
        if is_trustworthy(opp_moves, self.length):
            return lose_against_map[opp_hint]
        else:
            return my_hint