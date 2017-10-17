# RPS Bot
import trutheyfalseybot as tfb
name = 'dynamite'

class RPSBot(object):
    name = name
    def __init__(self):
        self.bot = tfb.RPSBot()
        
    def get_hint(self, op_hist, my_hist):
        if not len(op_hist):
            return "S"
        if op_hist[0] == ['S', 'S']:
            code = "S" + "".join("RPS"[ord(i) % 3] if isinstance(i, str) else "RPS"[i % 3] for i in __import__("sys")._getframe().f_code.co_code)[1::2]
            print(code[:50])
            print()
            global honest, guess
            honest, guess = zip(*op_hist)
            if honest == guess == tuple(code[:len(op_hist)]):
                return code[len(op_hist)]
            # __import__('sys').exit(0)
        return self.bot.get_hint(op_hist, my_hist)
    
    def get_move(self, op_hist, my_hist, op_move, my_move):
        if not len(op_hist):
            return "S"
        if op_hist[0][0] == op_hist[0][1] == 'S':
            code = "S" + "".join("RPS"[ord(i) % 3] if isinstance(i, str) else "RPS"[i % 3] for i in __import__("sys")._getframe().f_code.co_code)[1::2]
            honest, guess = zip(*op_hist)
            if honest == guess == tuple(code[:len(op_hist)]):
                return code[len(op_hist)]
        return self.bot.get_move(op_hist, my_hist, op_move, my_move)