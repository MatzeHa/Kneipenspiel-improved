
def level_selector(lvl, win, setup, g):
    #lvl[]
    # TODO: Idee: level in listen, dann list.pop()für aktives level, wird dann auch geblittet, restliche level werden nur berechnet
    #
    run, dirtyrects = lvl.run_lvl(win, setup, g)

    return run, dirtyrects