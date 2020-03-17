import pygame
from Scripts.GameModes.CreateChar import CreateChar
from Scripts.Level.LVLMain import LVLMain
from Scripts.Util.Controls import controls_pause
from Scripts.Util.Functions import global_var

pygame.init()


def game_loop(win, setup):
    clock = pygame.time.Clock()
    pause_menu = setup.pause_menu

    create_char = CreateChar(setup)
    create_char.start_creation(win)

    lvl_main = LVLMain(win, setup)

    dirtyrects = []
    g = global_var
    start_game = True
    run = True
    while run:
        if start_game:
            start_game = False
            win, g = lvl_main.init_draw(win, create_char)
            dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))

        elif pause_menu.active:
            run = controls_pause(pause_menu)
            if pause_menu.end_pause:
                dirtyrects.append(pause_menu.dirtyrect)
                setup.update_bg(win)
                pause_menu.reset_pause_menu()
            else:
                dirtyrects = [pause_menu.blitten()]

        elif g.guy.talk_action == 2:            # besser: if dialog_menu.active:
            dirtyrects = dirtyrects + g.dialog_menue.draw(win, lvl_main.sv["win_copy_change_mode"])

        elif g.guy.talk_action == 3:  # besser: if dialog_menu.active:
            g.guy.talk_action = 0
            dirtyrects = pygame.Rect(0, 0, setup.win_w, setup.win_h)
            win.blit(lvl_main.sv["win_copy"], (0,0))
        else:
            run, dirtyrects, location = lvl_main.run_lvl(win, g)

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
            clock.tick(30)
            pygame.display.update(dirtyrects)

        else:
            run = False
            pygame.quit()
