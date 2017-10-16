# RPS bot

import random
name = 'adaptivebot'
class RPSBot(object):
    name = name
    def __init__(self):
        self.winners = {"R": "P", "P": "S", "S": "R"}
    
    def get_hint(self, other_past, my_past):
        is_other_constant = len(set([other_claim for other_claim, other_move in other_past[-2:]])) == 1
        return self.winners[other_past[-1][0]] if is_other_constant else random.choice(list(self.winners.keys()))
    
    def get_move(self, other_past, my_past, other_next, my_next):
        is_other_honest = all([other_claim == other_move for other_claim, other_move in other_past[-2:]])
        return self.winners[other_next] if is_other_honest else my_next