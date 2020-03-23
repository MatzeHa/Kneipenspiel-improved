from Scripts.Util.Obstacles import Door

def level_selector(win, setup, g, lvl, lvl_name):
    run = True
    lvl_name, dirtyrects, travelling = player_travel(win, setup, g, lvl, lvl_name)
    dirtyrects = dirtyrects + npc_travel(win, setup, g, lvl)
    for _lvl in lvl:
        if "guy" in lvl[_lvl].chars:

            run, dirtyrect = lvl[_lvl].run_lvl(win, setup, g, travelling)
            dirtyrects = dirtyrects + dirtyrect
        else:
            lvl[_lvl].movement_calculation(win, setup, g)
    return [run, dirtyrects, lvl_name]


def load_level(win, setup, g, lvl, char):
    if char.travel not in lvl:
        if char.travel == "lvl_kitchen":
            from Scripts.Level.LVL1.LVLKitchen import LVLKitchen
            lvl[char.travel] = LVLKitchen(win, setup)
            lvl[char.travel].init_main(win, setup, g)

def npc_travel(win, setup, g, lvl):
    waiters = []
    guests = []
    dirtyrects = []
    for _lvl in lvl:
        waiters = waiters + [(w, lvl[_lvl].chars["waiter"].index(w)) for w in lvl[_lvl].chars["waiter"] if w.travel]
        guests = guests + [(g, lvl[_lvl].chars["guests"].index(g)) for g in lvl[_lvl].chars["guests"] if g.travel]
    for w in waiters:
        if w[0].travel == "lvl_outside":
            w[0].travel = False
            break
        if "guy" in lvl[w[0].location].chars:
            dirtyrects.append(w[0].del_blit(win, lvl[w[0].location].win_copy))
            dirtyrects.append(w[0].del_display(win, lvl[w[0].location].win_copy))
            dirtyrects.append(w[0].del_text(win, lvl[w[0].location].win_copy))
        load_level(win, setup, g, lvl, w[0])
        lvl[w[0].travel].chars["waiter"] = lvl[w[0].travel].chars["waiter"] + [lvl[w[0].location].chars["waiter"].pop(w[1])]
        lvl[w[0].travel].set_char_position(w[0], w[0].location)
        w[0].location = w[0].travel
        w[0].travel = False
    return dirtyrects



def player_travel(win, setup, g, lvl, old_room):
    dirtyrects = []
    # check if player wants to travel
    if lvl[old_room].chars["guy"].travel:
        # check if level has to be loaded
        load_level(win, setup, g, lvl, lvl[old_room].chars["guy"])
        if not setup.travel_door.opened:
            return old_room, dirtyrects, True

        else:
            # setup.travel_door.activated = True
            new_room = lvl[old_room].chars["guy"].travel
            lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")
            lvl[new_room].set_char_position(lvl[new_room].chars["guy"], lvl[new_room].chars["guy"].location)
            lvl[new_room].chars["guy"].location = new_room
            dirtyrects = lvl[new_room].reentry(setup, win)
            lvl[new_room].chars["guy"].travel = False
            if not lvl[new_room].loaded:
                lvl[new_room].init_draw(win, setup, g)
            for door in filter(lambda x: isinstance(x, Door), lvl[new_room].interactables):
                if door.goto == old_room:
                    door.opened = True
                    door.openCount = 40

            return new_room, dirtyrects, False
    else:
        return old_room, dirtyrects, False
