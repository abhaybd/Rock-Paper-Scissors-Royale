def play_match(bot1, bot2, n_rounds):
    win_against_map = {'R':'S', 'S':'P', 'P':'R'}
    global bot1_hist
    global bot2_hist
    bot1_hist = []
    bot2_hist = []
    bot1_match_score = 0
    bot2_match_score = 0
    for i in range(n_rounds):
        hint1 = bot1.get_hint(bot2_hist, bot1_hist)
        hint2 = bot2.get_hint(bot1_hist, bot2_hist)
        
        move1 = bot1.get_move(bot2_hist, bot1_hist, hint2, hint1)
        move2 = bot2.get_move(bot1_hist, bot2_hist, hint1, hint2)
        
        bot1_hist.append([hint1, move1])
        bot2_hist.append([hint2, move2])
        
        print('{} {}   |   {} {}'.format(hint1, hint2, move1, move2))
        
        if hint1 == move1:
            bot1_match_score += 1
        if hint2 == move2:
            bot2_match_score += 1
            
        if win_against_map[move1] == move2:
            bot1_match_score += 2
        elif win_against_map[move2] == move1:
            bot2_match_score += 2
        else:
            bot1_match_score += 1
            bot2_match_score += 1
    return bot1_match_score, bot2_match_score

import ann_bot as bot1_module
import rlbot as bot2_module
bot1 = bot1_module.RPSBot()
bot2 = bot2_module.RPSBot()

score1, score2 = play_match(bot1, bot2, 250)
print('{}-{}'.format(score1, score2))