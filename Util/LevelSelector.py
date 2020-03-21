


def level_selector(win, setup, lvl, lvl_name, g):
    # TODO: Idee: level in listen, dann list.pop()für aktives level, wird dann auch geblittet, restliche level werden nur berechnet

    run = True

    lvl_name, dirtyrects = travel_fun(win, setup, g, lvl, lvl_name)

    for _lvl in lvl:
        if "guy" in lvl[_lvl].chars:
            run, dirtyrect = lvl[_lvl].run_lvl(win, setup, g)
            dirtyrects = dirtyrects + dirtyrect
#            if changed:
#                dirtyrects = lvl[_lvl].reentry(setup)

        else:
            lvl[_lvl].movement_calculation(win, setup, g)

    return [run, dirtyrects, lvl_name]


def travel_fun(win, setup, g, lvl, old_room):
    dirtyrects = []
    if lvl[old_room].chars["guy"].travel:
        new_room = lvl[old_room].chars["guy"].travel
        lvl[old_room].chars["guy"].travel = False

        if new_room == "lvl_kitchen":
            if new_room not in lvl:
                from Scripts.Level.LVL1.LVLKitchen import LVLKitchen
                lvl[new_room] = LVLKitchen(win, setup, lvl[old_room].clock)
                lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")
                lvl[new_room].init_draw(win, setup, g)

                dirtyrects = lvl[new_room].reentry(setup, win)

            else:
                lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")
                dirtyrects = lvl[new_room].reentry(setup, win)


        elif new_room == "lvl_main":
            lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")
            dirtyrects = lvl[new_room].reentry(setup, win)

        return new_room, [dirtyrects]

    else:
        return old_room, []
