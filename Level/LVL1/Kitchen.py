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
        wall_w = 640
        wall_h = 110
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
            if _i.art == 'door' or _i.art == 'stairs':
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
        win_copy = win.copy()

        timer_clock = pygame.time.Clock()

        pygame.display.update()
        return timer_clock, guests, waiter, interactables, obstacles, win_copy

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

    def controls(self, g):
        run = True
        schachtel_oben = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        if keys[pygame.K_UP]:
            g.guy.sit = False
            g.guy.facing = 0
            g.guy.dir = 0
            g.guy.walk(self.waiter + self.guests, self.obstacles, self.interactables, self.sv["win_w"],
                       self.sv["win_h"],
                       self.sv["wall_w"], self.sv["wall_h"])
        elif keys[pygame.K_RIGHT]:
            g.guy.sit = False
            g.guy.facing = 1
            g.guy.dir = 1
            g.guy.walk(self.waiter + self.guests, self.obstacles, self.interactables, self.sv["win_w"],
                       self.sv["win_h"],
                       self.sv["wall_w"], self.sv["wall_h"])
        elif keys[pygame.K_DOWN]:
            g.guy.sit = False
            g.guy.facing = 2
            g.guy.dir = 2
            g.guy.walk(self.waiter + self.guests, self.obstacles, self.interactables, self.sv["win_w"],
                       self.sv["win_h"],
                       self.sv["wall_w"], self.sv["wall_h"])
        elif keys[pygame.K_LEFT]:
            g.guy.sit = False
            g.guy.facing = 3
            g.guy.dir = 3
            g.guy.walk(self.waiter + self.guests, self.obstacles, self.interactables, self.sv["win_w"],
                       self.sv["win_h"],
                       self.sv["wall_w"], self.sv["wall_h"])
        elif keys[pygame.K_e]:

            active_inter = dir_check(self.interactables, g.guy)
            if active_inter != 0:
                if active_inter.art == "door":
                    if active_inter.art == "door":
                        if active_inter.goto == "schachtel_oben":
                            schachtel_oben = True
                            run = False

                        active_inter.active = True
                        active_inter.openClose = True
                elif active_inter.art == "chair":
                    print("HINSETZEN")
                    if not g.guy.sit and not active_inter.active:
                        g.guy.sit_down(active_inter)
                #                            for i in dirtyrect:
                #                                dirtyrects.append(i)

                # active_inter.active = True
                #                        else:
                #                            textwin.text_count = 0
                #                            textwin.talker = active_inter.sit
                #                            textwin.text = 'Hey, schubs nicht so!'

                elif active_inter.art == "radio":
                    active_inter.active = not active_inter.active
                    if active_inter.active:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

        return run, schachtel_oben

    def run_lvl(self, win, g, lvl_before):
        #        self.win_copy, timer_clock, guests, waiter, interactables, obstacles = init_draw(win)

        pygame.mixer.music.set_volume(0.3)

        schachtel_oben = False
        run = True
        while run:
            _dirtyrects, run, schachtel_oben = self.redraw_game_window(win, g)

            self.timer_clock.tick(30)
            pygame.display.update(_dirtyrects)
        if schachtel_oben:
            g.guy.x = lvl_before.sv["coord"]["w"][3]
            g.guy.y = lvl_before.sv["coord"]["h"][11]
            g.guy.facing = 0
            win.blit(lvl_before.sv["win_copy"], (0, 0))
            pygame.display.update()
            lvl_before.run_lvl(win, g)