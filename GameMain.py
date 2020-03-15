import pygame
import os

from GameModes.PauseMenu import PauseMenu
from Util.GameLoop import game_loop
from Util.Functions import get_coords

pygame.init()

if __name__ == "__main__":
    class Setup:
        def __init__(self, win, win_w, win_h):
            self.win_w = win_w
            self.win_h = win_h
            self.win_size = (self.win_w, self.win_h)
            self.bgcol = (0, 0, 255)
            self.pause_menu = PauseMenu(win, self)
            self.wall_w = 150
            self.wall_h = 150
            self.cell_size = 64
            self.coord = {"w": get_coords(self.win_w, self.wall_w, self.cell_size),
                          "h": get_coords(self.win_h, self.wall_h, self.cell_size)}
            self.win_copy = win.copy()


        def update_bg(self, _win): # unnötige Funktion???
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
