import pygame
import math

from Scripts.Util.Functions import get_floor_pos, get_wall_size, get_bg_pos, get_coords, get_max_coord, draw_interactables, Raster

from Scripts.Util.Controls import controls_game

pygame.init()


class Level:
    def __init__(self, win, setup, name, obst_images, lvl_size, ground_size, enter_coord):
        self.name = name

        bg_pos = get_bg_pos(setup, lvl_size)
        wall_w, wall_h = get_wall_size(lvl_size, ground_size)
        floor_pos = get_floor_pos(bg_pos, lvl_size, wall_w, wall_h)

        coords = {"w": get_coords(floor_pos[0], floor_pos[2], setup.cell_size),
                  "h": get_coords(floor_pos[1], floor_pos[3], setup.cell_size)}
        # TODO: self.... , STATICVARS großs schreiben!!!

        self.sv = {"obst_images": obst_images,
                   "lvl_size": bg_pos,
                   "floor_pos": floor_pos,
                   "wall_w": wall_w,
                   "wall_h": wall_h,
                   "cell_size": setup.cell_size,        # TODO: soll bei setup alleine bleiben
                   "coord": coords,
                   "max_coord": get_max_coord(coords),
                   "enter_coord": enter_coord
                   }

        self.win_copy = win.copy()
        self.win_copy_change_mode = win.copy()
        self.active_IA = []  # active Interactables
        self.chars = {"guests": [],
                      "waiter": []
                      }
        self.lvl_vars = {}

    def movement_calculation(self, win, setup, g):
        print(self.name + "MOVEMENT CALCULATION")
        _dirtyrects = []

        # all interactables with own animation
        for i in self.active_IA:
            _dirtyrects.append(i.calc())

        # CALCULATE MOVEMENTS
        # guy
        if "guy" in self.chars:
            _dirtyrects.append(self.chars["guy"].calc_movement(win, self.chars, g))
        # Waiter
        for waiter in self.chars["waiter"]:
            _dirtyrects.append(waiter.calc_movement(self.chars, g, self.sv["coord"][self.sv["max_coord"]],
                                                    setup.win_w, setup.win_h,
                                                    self.sv["wall_w"], self.sv["wall_h"],
                                                    self.lvl_vars["door_pos"], self.sv["cell_size"],
                                                    self.lvl_vars["clock"], self.lvl_vars["obstacles"],
                                                    self.lvl_vars["interactables"]))
        # Guests
        for guest in self.chars["guests"]:
            if guest.walk_in[0] == self.lvl_vars["clock"].h_m[0] and guest.walk_in[1] <= self.lvl_vars["clock"].h_m[1] \
                    or guest.walk_in[0] < self.lvl_vars["clock"].h_m[0]:
                _dirtyrects.append(guest.calc_movement(self.chars, g, self.sv["coord"][self.sv["max_coord"]],
                                                       setup.win_w, setup.win_h,
                                                       self.sv["wall_w"], self.sv["wall_h"],
                                                       self.sv["cell_size"], self.active_IA,
                                                       self.lvl_vars["clock"], self.lvl_vars["obstacles"],
                                                       self.lvl_vars["interactables"], self.lvl_vars["door_pos"]))
        # CALCULATE DIRTYRECTS FOR DISPLAY
        for waiter in self.chars["waiter"]:
            _dirtyrects.append(waiter.calc_display())  # Display Waiter
        for i in self.chars["guests"]:
            if i.inside:
                _dirtyrects.append(i.calc_display())  # Display Gäste

        return _dirtyrects

    def del_last_blit(self, win, setup, g):
        dirtyrects = []
        if "guy" in self.chars:
            # wenn OrderMenue aufgemacht wird, wird eine Kopie des gesamten Bildes gespeichert
            if self.chars["guy"].orderAction == 5:
                # self.win_copy
                self.chars["guy"].orderAction = 6

            # wenn OrderMenue geschlossen wird, wird das Bild mit  der Kopie üüberblittet
            elif self.chars["guy"].orderAction == 7:
                win.blit(self.win_copy, (0, 0))
                dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))
                self.chars["guy"].orderAction = 8

            # wenn Dialog Menue aufgemacht wird, wird eine Kopie des gesamten Bildes gespeichert
            elif self.chars["guy"].talk_action == 1:
                self.sv["win_copy_change_mode"] = win.copy()
                g.dialog_menue.active = True
                self.chars["guy"].talk_action = 2

            # überblitten mit alter Kopie
            elif self.chars["guy"].talk_action == 2:
                win.blit(self.win_copy, (0, 0))
                dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))
            else:
                dirtyrects.append(self.chars["guy"].del_blit(win, self.win_copy))  # guy
                dirtyrects.append(self.chars["guy"].del_display(win, self.win_copy))  # Display guy
                if self.chars["guy"].text_count < 51:  # Textzeile wieder überblitten
                    dirtyrects.append(self.chars["guy"].del_text(win, self.win_copy))

                for waiter in self.chars["waiter"]:
                    dirtyrects.append(waiter.del_blit(win, self.win_copy))  # Waiter
                    dirtyrects.append(waiter.del_display(win, self.win_copy))  # Display Waiter
                    if waiter.text_count < 51:  # Textzeile wieder überblitten
                        dirtyrects.append(waiter.del_text(win, self.win_copy))

                for i in self.chars["guests"]:
                    dirtyrects.append(i.del_blit(win, self.win_copy))  # Guests
                    dirtyrects.append(i.del_display(win, self.win_copy))  # Display Waiter
                    if i.text_count < 51:  # Textzeile wieder überblitten
                        dirtyrects.append(i.del_text(win, self.win_copy))

            dirtyrects = dirtyrects + self.del_lvl_specials(win)
        return dirtyrects

    def del_lvl_specials(self, win):
        return []

    def draw_blits(self, win, g):
        _dirtyrects = []
        self.lvl_vars["clock"].draw(win)
        for i in self.active_IA:
            draw_interactables(win, self.win_copy, i)

        # characters
        self.chars["guy"].draw_char(win)
        for waiter in self.chars["waiter"]:
            waiter.draw_char(win)
        for guest in self.chars["guests"]:
            if guest.walk_in[0] == self.lvl_vars["clock"].h_m[0] and \
                    guest.walk_in[1] <= self.lvl_vars["clock"].h_m[1] or \
                    guest.walk_in[0] < self.lvl_vars["clock"].h_m[0]:
                guest.draw_char(win)

        #           Zeichnen - Balken und Text
        self.chars["guy"].draw_display(win, self.chars["guy"].drunkenness)  # Display guy
        for waiter in self.chars["waiter"]:
            waiter.draw_display(win, waiter.angryness)  # Display guy
        for i in self.chars["guests"]:
            if i.inside:
                _dirtyrects.append(i.draw_display(win, i.drunkenness))  # Display Gäste

        # Zeige Text an
        if self.chars["guy"].text_count < 50:
            _dirtyrects.append(self.chars["guy"].talk(win))
        for waiter in self.chars["waiter"]:
            if waiter.text_count < 50:
                _dirtyrects.append(waiter.talk(win))
        for i in self.chars["guests"]:
            if i.text_count < 50:
                _dirtyrects.append(i.talk(win))

        # Filter für Lichteffekte
        self.lvl_vars["halo_count"] += 1
        if self.lvl_vars["halo_count"] >= 100:  # pi *30
            self.lvl_vars["halo_count"] = 0
        self.lvl_vars["filter_halo"].set_alpha(round(math.sin((self.lvl_vars["halo_count"] / 100) * math.pi) * 100))
        win.blit(self.lvl_vars["filter_halo"], (0, 0))

        self.draw_blits_specials(win, g)

    def draw_blits_specials(self, win, g):
        pass

    def init_main(self, win, setup, create_char):
        return {}

    def init_draw(self, win, setup, g, create_char=None):
        win.fill((0, 0, 0), (0, 0, setup.win_w, setup.win_h))
        win.blit(self.lvl_vars["images"].bg_walls, (self.sv["lvl_size"][0], self.sv["lvl_size"][1]))
        win.blit(self.lvl_vars["images"].img_ground, (self.sv["lvl_size"][0] + self.sv["wall_w"],
                                                      self.sv["lvl_size"][1] + self.sv["wall_h"]))

        # get elements from init_main
        ret_dict = self.init_main(win, setup, create_char)

        # Blit Objects and make a copy of the Screen
        for obst in ret_dict["obstacles"]:
            win.blit(obst.pic, (obst.x, obst.y))
        self.win_copy = win.copy()

        # Blit Interactables and Clock
        for inter in ret_dict["interactables"]:
            if inter.art == 'door' or inter.art == "radio":
                inter.draw_int(win, self.win_copy)
                self.active_IA.append(inter)
            else:
                inter.draw(win)
        if "clock" in ret_dict:
            ret_dict["clock"].calc()
            ret_dict["clock"].draw(win)
            self.active_IA.append(ret_dict["clock"])

        # Create Raster
        Raster(win, self.sv["wall_w"], self.sv["wall_h"], self.sv["floor_pos"], self.sv["lvl_size"], self.sv["cell_size"])
        # make Copy
        self.win_copy = win.copy()

#        self.chars["guy"].x, self.chars["guy"].y =

        # adding everything created to self.lvl_vars        ====> must haves!!! <====
        self.lvl_vars["obstacles"] = ret_dict["obstacles"]
        self.lvl_vars["interactables"] = ret_dict["interactables"]
        self.lvl_vars["door_pos"] = ret_dict["door_pos"]
        self.lvl_vars["filter_halo"] = ret_dict["filter_halo"]


        # adding level specific items
        self.init_draw_specials(win, setup, g, create_char, ret_dict)


    def init_draw_specials(self, win, setup, g, create_char, ret_dict):
        pass

    def reentry(self, setup):
        self.chars["guy"].x, self.chars["guy"].y = self.sv["enter_coord"]

        return pygame.Rect(0, 0, setup.win_w, setup.win_h)

    def run_lvl(self, win, setup, g):

        dirtyrects = []

        # Controls:
        run = controls_game(setup, self.chars, g, self.lvl_vars["obstacles"], self.lvl_vars["interactables"], self.sv)

        # Overblit with former State
        dirtyrects = dirtyrects + self.del_last_blit(win, setup, g)

        # Calculations
        dirtyrects = dirtyrects + self.movement_calculation(win, setup, g)

        # Blit actual State
        self.draw_blits(win, g)

        return run, dirtyrects
