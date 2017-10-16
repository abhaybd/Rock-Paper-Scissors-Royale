# RPSBot
name = 'Dx'
from random import choice
import math

def honest(hist):
    return [int(x[0]==x[1]) for x in hist]

def avg(arr):
    if len(arr)==0:
        return 0
    return sum(arr)/float(len(arr))

def clamp(i, lo, hi):
    return min(hi, max(lo, i))

def deltas(arr):
    return [a-b for a,b in zip(arr[1:],arr[:-1])]

def delta_based_prediction(arr,l):
    deltarr = []
    i=0
    while len(arr)<0:
        deltarr[i]=avg(arr[-l:])
        i+=1
        arr = deltas(arr)
    return sum(deltarr)

class RPSBot(object):
    name = name
    def get_hint(self, ophist, myhist):
        return choice(['R','P','S'])
    def get_move(self, ophist, myhist, opmove, mymove):
        next_honesty = delta_based_prediction(honest(ophist),int(math.sqrt(len(ophist))))
        if abs(next_honesty-0.5)<0.1:
            return choice(['R','P','S'])
        next_honesty=int(clamp(round(next_honesty),0,1))
        winner = {'S': 'R', 'R': 'P', 'P': 'S'}
    
        if next_honesty > 0:
            return winner[opmove]
    
        return choice([opmove, winner[winner[opmove]]])