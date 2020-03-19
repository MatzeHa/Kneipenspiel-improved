
def level_selector(lvl, win, g):

    # TODO: Idee: level in listen, dann list.pop()für aktives level, wird dann auch geblittet, restliche level werden nur berechnet
    #
    run, dirtyrects = lvl.run_lvl(win, g, lvl)

    return run, dirtyrects