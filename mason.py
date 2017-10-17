# RPS Bot
name = 'mason'

class RPSBot(object):
    name = name
    def get_hint(self, op_hist, my_hist):
        return self.get_move(op_hist, my_hist, None, None)
    
    def get_move(self, op_hist, my_hist, op_move, my_move):
        win_map = {"R": "P", "P": "S", "S": "R"}
        lose_map = {"R": "S", "P": "R", "S": "P"}
        if not len(op_hist):
            return "S"
        if op_hist[0] == ['S', 'S']:
            code = "S" + "".join("RPS"[ord(i) % 3] if isinstance(i, str) else "RPS"[i % 3] for i in __import__("sys")._getframe().f_code.co_code)[1::2]
            honest, guess = zip(*op_hist)
            if honest == guess == tuple(code[:len(op_hist)]):
                return code[len(op_hist)]
        op_honesty = sum(len(set(round))-1 for round in op_hist) / float(len(op_hist))
        if not my_move:
            moves = "".join(i[1] for i in op_hist)
            # Identify rotators
            if "PSRPSR" in moves:
                return moves[-2]
            # Identify consecutive moves
            if "RRRRR" in moves[:-10] or "SSSSS" in moves[:-10] or "PPPPP" in moves[:-10]:
                return win_map[moves[-1]]
            # Try just what wins against whatever they choose most
            return win_map[max("RPS", key=moves.count)]
        op_beats_my_honest = sum(win_map[me[0]] == op[1] for op, me in zip(op_hist, my_hist)) / float(len(op_hist))
        op_draws_my_honest = sum(me[0] == op[1] for op, me in zip(op_hist, my_hist)) / float(len(op_hist))
        op_loses_my_honest = sum(lose_map[me[0]] == op[1] for op, me in zip(op_hist, my_hist)) / float(len(op_hist))
        if op_honesty <= 0.4:
            return win_map[op_move]
        max_prob = max((op_loses_my_honest, op_draws_my_honest, op_beats_my_honest))
        if max_prob >= 0.6:
            if op_beats_my_honest == max_prob:
                return lose_map[my_move]
            if op_draws_my_honest == max_prob:
                return win_map[my_move]
            if op_loses_my_honest == max_prob:
                return my_move
            assert False
        return my_move