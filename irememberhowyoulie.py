# RPS Bot
name = 'irememberhowyoulie'
import random
class RPSBot(object):
    name = name
    def __init__(self):
        random.seed()
        self.wintable = {
                    "R": {"R": 1, "P": 0, "S": 2},
                    "P": {"R": 2, "P": 1, "S": 0},
                    "S": {"R": 0, "P": 2, "S": 1}
                   }
        self.winprob = {
                   "R": {"R": 0.0, "P": 0.0, "S": 0.0},
                   "P": {"R": 0.0, "P": 0.0, "S": 0.0},
                   "S": {"R": 0.0, "P": 0.0, "S": 0.0}
                  }
        self.totalprob = {"R": 0, "P": 0, "S": 0}
        
    def get_hint(self, opponentlist, mylist):
        picklength = min(random.randint(15, 25), len(opponentlist))
        lying, tempsum = 0, 0.0
        pickedup = {"R": 0, "P": 0, "S": 0}
        if picklength == 0:
            lying = 0.5
        else:
            for eachround in opponentlist[-picklength:]:
                pickedup[eachround[1]] += 1
                if eachround[0] != eachround[1]:
                    lying += 1
            lying = lying * 1.0 / picklength
        for s in pickedup:
            pickedup[s] = 1.0 / (1 + pickedup[s])
            tempsum += pickedup[s]
        a = random.random() * tempsum
        if a < pickedup["R"]:
            return "R"
        elif a < pickedup["R"] + pickedup["P"]:
            return "P"
        else:
            return "S"
        
    def get_move(self, opponentlist, mylist, opponentmove, mymove):
        picklength = min(random.randint(15, 25), len(opponentlist))
        lying, tempsum = 0, 0.0
        pickedup = {"R": 0, "P": 0, "S": 0}
        if picklength == 0:
            lying = 0.5
        else:
            for eachround in opponentlist[-picklength:]:
                pickedup[eachround[1]] += 1
                if eachround[0] != eachround[1]:
                    lying += 1
            lying = lying * 1.0 / picklength
        for s in pickedup:
            pickedup[s] = 1.0 / (1 + pickedup[s])
            tempsum += pickedup[s]
        for me in self.winprob:
            ishonest = 0
            if me == mymove:
                ishonest = 1
            for op in self.winprob[me]:
                if op == opponentmove:
                    self.winprob[me][op] = (self.wintable[me][op] + ishonest) * (1 - lying)
                else:
                    self.winprob[me][op] = (self.wintable[me][op] + ishonest) * lying * pickedup[op] / (tempsum - pickedup[opponentmove])
                self.totalprob[me] += self.winprob[me][op]

        optimalmove, optimalvalue = "R", -9999999.0
        for me in self.totalprob:
            if self.totalprob[me] > optimalvalue:
                optimalmove, optimalvalue = me, self.totalprob[me]
        return optimalmove