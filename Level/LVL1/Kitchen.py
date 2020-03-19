import pygame
import sys

from Scripts.Util.Obstacles import Obstacle, Door, Radio
from Scripts.Util.LoadImages import ObstacleImages
from Scripts.Util.DirCheck import dir_check
from Scripts.Util.Functions import IncreaseI, get_coords, get_max_coord, Raster

pygame.init()

drinks = {0: ("", 0, 0, 0), 1: ("Bier", 3, 10, 10), 2: ("Wein", 4, 5, 5), 3: ("Schnaps", 2, 30, 1),
          4: ("Kaffee", 3, -3, 6)}


class LVLKitchen:
    def __init__(self, win):
        win_w, win_h = win.get_size()

        cell_size = 64
        coord = {"w": get_coords(win_w, wall_w, cell_size),
                 "h": get_coords(win_h, wall_h, cell_size)}
        self.sv = {"images": ObstacleImages(),
                   "win_w": win_w,
                   "win_h": win_h,
                   "wall_w": wall_w,
                   "wall_h": wall_h,
                   "cell_size": cell_size,
                   "coord": coord,
                   "max_coord": get_max_coord(coord),
                   "raster": Raster(win, wall_w, wall_h, cell_size)
                   }
        self.door_pos = []
        self.timer_clock, self.guests, self.waiter, self.interactables, self.obstacles, self.win_copy = self.init_draw(
            win)

    def init_kitchen(self):
        # Obstacles und Interactables werden erstellt
        _obstacles = []
        _interactables = []

        i = IncreaseI()
        _interactables.append(
            Door(i.increase(), self.sv["coord"]["w"][4], self.sv["coord"]["h"][0],
                 self.sv["images"].img_door[0].get_width(),
                 self.sv["images"].img_door[0].get_height(),
                 180, self.sv["coord"], self.sv["cell_size"], "schachtel_oben"))

        _door_pos = []
        for _i in _interactables:
            if _i.art == 'door':
                _door_pos.append(_i.serv_pos)

        _obstacles.append(
            Obstacle(i.increase(), "Walls_add", self.sv["images"].walls_add1,
                     self.sv["coord"]["w"][0], self.sv["coord"]["h"][0],
                     self.sv["images"].walls_add1.get_width(), self.sv["images"].walls_add1.get_height()))
        return _interactables, _obstacles

    def init_draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (0, 0, self.sv["win_w"], self.sv["win_h"]))
        pygame.draw.rect(win, (10, 80, 225), (self.sv["wall_w"], self.sv["wall_h"],
                                              self.sv["win_w"] - 2 * self.sv["wall_w"],
                                              self.sv["win_h"] - 2 * self.sv["wall_h"]))
        interactables, obstacles = self.init_kitchen()
        guests = []
        waiter = []

        self.sv["raster"].draw(win)

        for obst in obstacles:
            win.blit(obst.pic, (obst.x, obst.y))
        win_copy = win.copy()

        for inter in interactables:
            if isinstance(inter, Door) or isinstance(inter, Radio):
                inter.draw_int(win, win_copy)
            else:
                inter.draw(win)

        # adding everything created to self.lvl_vars        ====> must haves!!! <====
        self.lvl_vars["obstacles"] = ret_dict["obstacles"]
        self.lvl_vars["interactables"] = ret_dict["interactables"]
        self.lvl_vars["door_pos"] = ret_dict["door_pos"]
        self.lvl_vars["clock"] = ret_dict["clock"]
        self.lvl_vars["raster"] = raster
        self.lvl_vars["filter_halo"] = ret_dict["filter_halo"]

        #return timer_clock, guests, waiter, interactables, obstacles, win_copy

    def init_draw_specials(self, win, setup, create_char, g, ret_dict):
        pass




    def redraw_game_window(self, win, g):
        dirtyrects = self.del_last_blit(win, g)

        if g.guy.text_count < 51:  # Textzeile wieder überblitten
            dirtyrects.append(g.guy.del_text(win, self.win_copy))

        _run, _schachtel_oben = self.controls(g)
        dirtyrects = dirtyrects + self.movement_calculcation(win, g)
        g.guy.draw_char(win)
        return dirtyrects, _run, _schachtel_oben

    def movement_calculcation(self, win, g):
        dirtyrects = []
        # all interactables with own animation
        for _inter in self.interactables:
            if _inter.active:
                if isinstance(_inter.active, Door) or isinstance(_inter.active, Radio):
                    dirtyrects.append(_inter.calc())
                    _inter.draw_int(win, self.win_copy)
        #        _dirtyrects.append(_clock.calc())
        # Guy
        dirtyrects.append(g.guy.calc_movement(win, drinks))

        return dirtyrects

    def del_last_blit(self, win, g):
        dirtyrects = list()
        dirtyrects.append(g.guy.del_blit(win, self.win_copy))  # Guy
        dirtyrects.append(g.guy.del_display(win, self.win_copy))  # Display Guy
        return dirtyrects

