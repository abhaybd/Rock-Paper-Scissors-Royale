# RPS controller

def get_bots():
    import os
    from os.path import isfile, dirname, abspath
    bots = []
    exceptions = {'ann_bot', 'dynamite', 'Dx', 'averager', 'irememberhowyoulie', '1v1'}
    for module in os.listdir(dirname(abspath(__file__))):
        name = module[:-3]
        if not isfile(module) or module[-3:] != '.py' or module == '__init__.py' or module == __file__.split('/')[-1] or name in exceptions:
            continue
        imported = __import__(name, locals(), globals())
        if hasattr(imported, 'RPSBot'):
            bots.append(imported)
        else:
            del imported
    del os, module, isfile, dirname, abspath
    return bots

def round_robin(bot_modules):
    bot_scores = {bot_module.RPSBot():0 for bot_module in bot_modules}
    for bot1 in bot_scores.keys():
        for bot2 in bot_scores.keys():
            opponent = bot2
            if bot1 == bot2:
                opponent = [module.RPSBot() for module in bot_modules if module.name == bot1.name][0]
            score1, score2 = play_match(bot1, opponent, 250, bot_scores)
            winner = (bot1,score1)
            loser = (bot2,score2)
            if score2 > score1:
                winner = (bot2,score2)
                loser = (bot1,score1)
            print('{} beat {} {}-{}!'.format(winner[0].name, loser[0].name,
                  winner[1], loser[1]))
        print()
    return bot_scores

def play_match(bot1, bot2, n_rounds, bot_scores):
    win_against_map = {'R':'S', 'S':'P', 'P':'R'}
    global bot1_hist
    global bot2_hist
    bot1_hist = []
    bot2_hist = []
    bot1_match_score = 0
    bot2_match_score = 0
    if bot1 not in bot_scores:
        bot_scores[bot1] = 0
    if bot2 not in bot_scores and bot1.name != bot2.name:
        bot_scores[bot2] = 0
    for i in range(n_rounds):
        hint1 = bot1.get_hint(bot2_hist, bot1_hist)
        hint2 = bot2.get_hint(bot1_hist, bot2_hist)
        
        if not hint1:
            print('Player1 returned None for hint, automatically forfeits round')
            bot2_match_score += 3
            continue
        if not hint2:
            print('Player2 returned None for hint, automatically forfeits round')
            bot1_match_score += 3
            continue
        
        move1 = bot1.get_move(bot2_hist, bot1_hist, hint2, hint1)
        move2 = bot2.get_move(bot1_hist, bot2_hist, hint1, hint2)
        
        if not move1:
            print('Player1 returned None for move, automatically forfeits round')
            bot2_match_score += 3
            continue
        if not move2:
            print('Player2 returned None for move, automatically forfeits round')
            bot1_match_score += 3
            continue
        
        bot1_hist.append([hint1, move1])
        bot2_hist.append([hint2, move2])
        
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
    bot_scores[bot1] += bot1_match_score
    if bot1.name != bot2.name:
        bot_scores[bot2] += bot2_match_score
    return bot1_match_score, bot2_match_score        

bot_modules = get_bots()
print('Found {} unique bots!'.format(len(bot_modules)))
print('Starting round robin.', end = '\n\n')
bot_scores = round_robin(bot_modules)
bot_scores = {bot.name:bot_scores[bot] for bot in bot_scores.keys()}
n_games = len(bot_scores)*2-1
normalized_scores = {bot:bot_scores[bot]/n_games for bot in bot_scores.keys()}

leaderboard = sorted(list(normalized_scores), reverse = True, key = lambda x: normalized_scores[x])
for i, bot in enumerate(leaderboard):
    print('{}: {} - {}pts'.format(i+1, bot, normalized_scores[bot]))