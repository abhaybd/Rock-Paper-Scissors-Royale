# RPS Bot
name = 'two_thirds'
import random

class RPSBot(object):
    name = name
    def __init__(self):
        self.moves = {'R','P','S'}
    def get_hint(self, h_opp, h_me):
        return random.choice(list(self.moves))
    
    def get_move(self, h_opp, h_me, opp, me):
        res = self.result(opp, me)
        if res==-1:
            counter = list((self.moves - {opp, me}))[0]
            return random.choice([me,counter,counter])
        if res==1:
            return random.choice([me,me,opp])
        return me
    
    def result(self, opp, me):
        if opp==me: return 0
        if opp=="R" and me=="S" or opp=="S" and me=="P" or opp=="P" and me=="R": return -1
        return 1