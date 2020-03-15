import pygame
from Util.Controls import controls_game, controls_pause

pygame.init()



def game_loop(setup, g, run=True):
    clock = pygame.time.Clock()
    pause_menue = setup.pause_menu
    win = setup.win
    while run:
        # EINGABE
        if pause_menue.active:
            run = controls_pause(pause_menue)

            if pause_menue.end_pause:
                setup.dirtyrects.append(pause_menue.dirtyrect)
                setup.update_bg(win)
                pause_menue.reset_pause_menue()
            else:
                setup.dirtyrects = [pause_menue.blitten()]


        else:
            run = controls_game(setup, g)

        if not pause_menue.quit:
            clock.tick(30)
            pygame.display.update(setup.dirtyrects)
        else:
            pygame.quit()
            run = False
