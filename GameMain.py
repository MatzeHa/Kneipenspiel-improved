import os

import pygame
from Scripts.GameModes.PauseMenu import PauseMenu
from Scripts.GameModes.Dialog import DialogMenue
from Scripts.Util.Functions import get_coords
from Scripts.Util.GameLoop import game_loop

pygame.init()

if __name__ == "__main__":
    class Setup:
        def __init__(self, _win, _win_w, _win_h):
            self.win_w = _win_w
            self.win_h = _win_h
            self.wall_h = 150
            self.wall_w = 150
            self.win_size = (self.win_w, self.win_h)
            self.bgcol = (0, 0, 255)
            self.pause_menu = PauseMenu(_win, self)
            self.cell_size = 64
            self.coord = {"w": get_coords(self.win_w, self.wall_w, self.cell_size),
                          "h": get_coords(self.win_h, self.wall_h, self.cell_size)}
            self.win_copy = _win.copy()
            self.active_room = "Main"

        def update_bg(self, _win):  # unnötige Funktion???
            self.bgcol = setup.pause_menu.options["bgcol"]
            _win.fill(self.bgcol)
            self.win_copy = _win.copy()


    os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 30"
    pygame.display.set_caption("Matzes Kneipenspiel", "MK")
    win_w = 1900
    win_h = 1068
    win = pygame.display.set_mode((win_w, win_h))
    setup = Setup(win, win_w, win_h)

    pygame.mouse.set_visible(False)

    win.fill((50, 255, 255), (0, 0, 1000, 1000))
    pygame.display.update()

    game_loop(win, setup)
