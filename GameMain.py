import pygame
import os


from Scripts.GameModes.PauseMenu import PauseMenu
from Scripts.Level.LVLMain import LVLMain
from Scripts.Util.GameLoop import game_loop
from Scripts.GameModes.CreateChar import CreateChar
from Scripts.Util.Functions import get_coords

pygame.init()

if __name__ == "__main__":
    class Setup:
        def __init__(self):
            self.win = pygame.Surface((0, 0))
            self.dirtyrects = []
            self.win_w = 1900
            self.win_h = 1068
            self.win_size = (self.win_w, self.win_h)
            self.bgcol = (0, 0, 255)
            self.pause_menu = 0
            self.wall_w = 150
            self.wall_h = 150
            self.cell_size = 64
            self.coord = {"w": get_coords(self.win_w, self.wall_w, self.cell_size),
                          "h": get_coords(self.win_h, self.wall_h, self.cell_size)}

        def update_bg(self, _win):
            self.bgcol = setup.pause_menue.options["bgcol"]
            _win.fill(self.bgcol)
            self.win = _win.copy()

    setup = Setup()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 0"
    win = pygame.display.set_mode((setup.win_w, setup.win_h))
    pygame.display.set_caption("Matzes Kneipenspiel", "MK")
    setup.win = win.copy()

    '''
    entity = Entity()
    opponents = []
    for i in range(0, 5):
        opponents.append(Entity())
    '''

    setup.pause_menu = PauseMenu(win, setup)
    pygame.mouse.set_visible(False)

    create_char = CreateChar(setup)
    create_char.start_creation(win)



    lvl_main = LVLMain(win, setup)
    win, g = lvl_main.init_draw(win, create_char)

    game_loop(setup, g)