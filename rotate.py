# RPS Bot

name = 'rotate'
class RPSBot(object):
    name = name
    def get_hint(self, h1, h2):
        return ("R", "P", "S")[len(h1) % 3]
    def get_move(self, h1, h2, m1, m2):
        return self.get_hint(h1, h2)