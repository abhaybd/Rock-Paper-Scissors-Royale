# RPS Bot
name = 'RLBot'
def score(d,m1,m2):
    s=0
    if m1==m2:
        s=1
    elif (m1+m2) in "RPSR":
        s=2
    return s+(d==m2)
class RPSBot(object):
    name = name
    def __init__(self):
        self.alpha = 0.2
        
    def get_hint(self, hismoves, mymoves):
        bestscore=-1
        bestmove=""
        for move in "RPS":
            ev=3
            for (his,my) in zip(hismoves,mymoves):
                (d1,m1)=his
                (d2,m2)=my
                if d2==move:
                    ev=(1-self.alpha)*ev+self.alpha*score(d2,m1,m2)
            if ev>bestscore:
                bestscore=ev
                bestmove=move
        return bestmove
    
    def get_move(self, hismoves, mymoves, hismove, mymove):
        if mymove:
            history=[([d1,m1],[d2,m2]) for ((d1,m1),(d2,m2)) in zip(hismoves,mymoves) if score(None,hismove,mymove)==score(None,d1,d2)]
            bestscore=-1
            bestmove=""
            for move in "RPS":
                ev=2+(move==mymove)
                for ((d1,m1),(d2,m2)) in history:
                    if score(None,move,mymove)==score(None,m2,d2):
                        ev=(1-self.alpha)*ev+self.alpha*score(d2,m1,m2)
                if ev>bestscore:
                    bestscore=ev
                    bestmove=move
            return bestmove