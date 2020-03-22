


def level_selector(win, setup, lvl, lvl_name, g):
    run = True
    lvl_name, dirtyrects, changed = travel_fun(win, setup, g, lvl, lvl_name)
    char_travel_fun(lvl)
    for _lvl in lvl:
        if "guy" in lvl[_lvl].chars:
            run, dirtyrect = lvl[_lvl].run_lvl(win, setup, g, changed)
            dirtyrects = dirtyrects + dirtyrect
        else:
            lvl[_lvl].movement_calculation(win, setup, g)
    return [run, dirtyrects, lvl_name]

def char_travel_fun(lvl):
    for _lvl in lvl:

        for index, waiter in enumerate(lvl[_lvl].chars["waiter"]):
            if waiter.travel:
                lvl[waiter.travel].chars["waiter"] = lvl[_lvl].chars["waiter"].pop(index)


def travel_fun(win, setup, g, lvl, old_room):
    dirtyrects = []
    if lvl[old_room].chars["guy"].travel:
        if setup.travel_counter < 50:
            setup.travel_counter += 1
            return old_room, [], True

        else:
            new_room = lvl[old_room].chars["guy"].travel

            if new_room == "lvl_kitchen":
                if new_room not in lvl:
                    from Scripts.Level.LVL1.LVLKitchen import LVLKitchen
                    lvl[new_room] = LVLKitchen(win, setup, lvl[old_room].clock)
                    lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")
                    lvl[new_room].init_draw(win, setup, g)

                    dirtyrects = lvl[new_room].reentry(setup, win, old_room)

                else:
                    lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")
                    dirtyrects = lvl[new_room].reentry(setup, win, old_room)


            elif new_room == "lvl_main":
                lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")
                dirtyrects = lvl[new_room].reentry(setup, win, old_room)

            lvl[new_room].chars["guy"].travel = False
            return new_room, [dirtyrects], False
    else:
        return old_room, [], False
