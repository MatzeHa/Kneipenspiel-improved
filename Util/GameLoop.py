import pygame
from Scripts.GameModes.CreateChar import CreateChar
from Scripts.Level.LVL1.LVLMain import LVLMain

from Scripts.Util.Controls import controls_pause, controls_maxle, controls_dialog, controls_order
from Scripts.Util.Functions import global_var, show_dirtyrects
from Scripts.Util.LevelSelector import level_selector

pygame.init()


def game_loop(win, setup):
    clock = pygame.time.Clock()
    pause_menu = setup.pause_menu


    create_char = CreateChar()
#      create_char.start_creation(win, setup)

    # lvl = [LVLMain(win, setup), ]

    lvl = {"lvl_main": LVLMain(win, setup)}
    lvl_name = "lvl_main"

    dirtyrects = []
    start_game = True
    run = True

    first_round = True

    g = global_var(setup)

    while run:
        if start_game:
            start_game = False
            lvl[lvl_name].init_main(win, setup, create_char)
            lvl[lvl_name].init_draw(win, setup, g)

            del create_char
            dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))

        elif pause_menu.active:
            run = controls_pause(pause_menu)
            dirtyrects = pause_menu.check_action(win, lvl[lvl_name])

        elif g.dialog_menue.active:
            g.dialog_menue = controls_dialog(g.dialog_menue)
            dirtyrects = g.dialog_menue.check_action(win, setup, lvl[lvl_name].chars, lvl[lvl_name])

        elif lvl[lvl_name].chars["guy"].orderAction == 6:
            lvl[lvl_name].chars["guy"].order_menue = controls_order(lvl[lvl_name].chars, g)
            dirtyrects.append(g.order_menue.draw(win, setup, g, lvl[lvl_name]))

        elif lvl[lvl_name].chars["guy"].game == "maxle":
            setup.game = controls_maxle(setup.game_maxle, lvl[lvl_name].chars["guy"], g.drinks)
            dirtyrects = setup.game.check_action(win, setup, lvl[lvl_name].chars, g, lvl[lvl_name])

        else:
            run, dirtyrects, lvl_name = level_selector(win, setup, g, lvl, lvl_name)

        if not pause_menu.quit:
            if first_round:
                first_round = False
            else:
                pass
                show_dirtyrects(win, dirtyrects)

            clock.tick(30)
            pygame.display.update(dirtyrects)

        else:
            run = False
            pygame.quit()

