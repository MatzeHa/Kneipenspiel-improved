import pygame
from Scripts.GameModes.CreateChar import CreateChar
from Scripts.Level.LVL1.LVLMain import LVLMain
from Scripts.Util.Controls import controls_pause, controls_maxle, controls_dialog, controls_order
from Scripts.Util.Functions import global_var, show_dirtyrects

pygame.init()


def game_loop(win, setup):
    clock = pygame.time.Clock()
    pause_menu = setup.pause_menu
    create_char = CreateChar(setup)
    create_char.start_creation(win)

    lvl = LVLMain(win, setup)

#    lvl = {"lvl_main": LVLMain(win, setup)}

    dirtyrects = []
    g = global_var
    start_game = True
    run = True

    first_round = True

    while run:
        if start_game:
            start_game = False
            win, g = lvl.init_draw(win, create_char)
            dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))

        elif pause_menu.active:
            run = controls_pause(pause_menu)
            dirtyrects = pause_menu.check_action(win, lvl)

        elif g.dialog_menue.active:
            g.dialog_menue = controls_dialog(g.dialog_menue)
            dirtyrects = g.dialog_menue.check_action(win, setup, g, lvl)

        elif g.guy.orderAction == 6:
            g.order_menue = controls_order(g)
            dirtyrects.append(g.order_menue.draw(win, setup, g, lvl))

        elif g.guy.game == "maxle":
            setup.game = controls_maxle(setup.game_maxle, g.guy, g.drinks)
            dirtyrects = setup.game.check_action(win, setup, g, lvl)

        else:
            run, dirtyrects = lvl.run_lvl(win, g, lvl)

        '''
        if kitchen:
            #            if lvl_kitchen not in locals():
            from Level.CreateKitchen import LVLKitchen
            lvl_kitchen = LVLKitchen(win)
            g.guy.x = lvl_kitchen.sv["coord"]["w"][7]
            g.guy.y = lvl_kitchen.sv["coord"]["h"][0]
            g.guy.facing = 2
            self.g = g
            lvl_kitchen.run_lvl(win, g, self)

        win.blit(self.sv["images"].game_over, (win_w / 2 - 400, win_h / 2 - 232))
        pygame.display.update()
        pygame.quit()
        '''

        if not pause_menu.quit:
            if first_round:
                first_round = False
            else:
                pass
                # show_dirtyrects(win, dirtyrects)

            clock.tick(30)
            pygame.display.update(dirtyrects)

        else:
            run = False
            pygame.quit()
