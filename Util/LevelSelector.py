from Scripts.Util.Functions import travel_fun


def level_selector(win, setup, lvl, lvl_name, g):
    #lvl[]
    # TODO: Idee: level in listen, dann list.pop()für aktives level, wird dann auch geblittet, restliche level werden nur berechnet
    run = True
    dirtyrects = []
    lvl_name = travel_fun(win, setup, g, lvl, lvl_name)

    for _lvl in lvl:
        if "guy" in lvl[_lvl].chars:
            run, dirtyrects = lvl[_lvl].run_lvl(win, setup, g)
        else:

            lvl[_lvl].movement_calculation(win, setup, g)

    return run, dirtyrects, lvl_name
