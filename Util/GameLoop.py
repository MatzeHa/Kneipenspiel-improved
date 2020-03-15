import pygame

from Level.LVLMain import LVLMain
from Util.Controls import controls_pause
from GameModes.CreateChar import CreateChar

pygame.init()


def game_loop(win, setup):
    clock = pygame.time.Clock()
    pause_menue = setup.pause_menu

    create_char = CreateChar(setup)
    create_char.start_creation(win)

    lvl_main = LVLMain(win, setup)

    dirtyrects = []
    start_game = True
    run = True
    while run:
        if start_game:
            start_game = False
            win, g = lvl_main.init_draw(win, create_char)
            dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))

        elif pause_menue.active:
            run = controls_pause(pause_menue)
            if pause_menue.end_pause:
                dirtyrects.append(pause_menue.dirtyrect)
                setup.update_bg(win)
                pause_menue.reset_pause_menue()
            else:
                dirtyrects = [pause_menue.blitten()]

        else:
            run, dirtyrects, location = lvl_main.run_lvl(win, setup, g)

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

        if not pause_menue.quit:
            clock.tick(30)
            pygame.display.update(dirtyrects)
        else:
            run = False
            pygame.quit()
