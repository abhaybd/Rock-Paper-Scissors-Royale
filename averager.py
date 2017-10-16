# RPS Bot
name = 'averager'
import random
class RPSBot(object):
    name = name
    def get_hint(self, op, mp):
        if len(op) == len(mp) == 0:
            return random.choice('RPS')
        else:
            opa = [i[1] for i in op]
            copa = [opa.count(i) for i in 'RPS']
            copam = [i for i, j in zip('RPS', copa) if j == max(copa)]
            opd = [i[0] for i in op]
            copd = [opd.count(i) for i in 'RPS']
            copm = [i for i, j in zip('RPS', copd) if j == max(copd) and i in copam]
            return random.choice(copam if copm == [] else copm)
    
    def get_move(self, op, mp, od, md):
        if len(op) == len(mp) == 0:
            return md
        else:
            hop = sum([1. if i[0] == i[1] else 0. for i in op]) / len(op)
            hmp = sum([1. if i[0] == i[1] else 0. for i in mp]) / len(mp)
            return 'PSR'['RPS'.index(od)] if hmp >= 0.75 and hop >= 0.50 else md