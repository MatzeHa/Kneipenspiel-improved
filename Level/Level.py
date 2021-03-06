import pygame
import math

from Scripts.Util.Functions import get_floor_pos, get_wall_size, get_bg_pos, get_coords, get_max_coord, draw_interactables, Raster

from Scripts.Util.Controls import controls_game

from Scripts.Util.Obstacles import Door


pygame.init()


class Level:
    def __init__(self, win, setup, name, obst_images, lvl_size, ground_size):
        self.clock = None
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
                   "coords": coords,
                   "max_coord": get_max_coord(coords)
                   }

        self.win_copy = win.copy()
        self.win_copy_change_mode = win.copy()
        self.active_IA = []  # active Interactables
        self.chars = {"guests": [],
                      "waiter": []
                      }
        self.lvl_vars = {}
        self.loaded = False

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
            _dirtyrects.append(waiter.calc_movement(self.chars, setup, self.sv["floor_pos"],
                                                    self.sv["coords"],
                                                    setup.cell_size,
                                                    self.clock, self.obstacles,
                                                    self.interactables, self.pos_goals))
        # Guests
        for guest in self.chars["guests"]:
            if guest.walk_in[0] == self.clock.h_m[0] and guest.walk_in[1] <= self.clock.h_m[1] \
                    or guest.walk_in[0] < self.clock.h_m[0]:
                _dirtyrects.append(guest.calc_movement(self.chars, g,
                                                       self.sv["coords"],
                                                       setup.win_w, setup.win_h,
                                                       self.sv["wall_w"], self.sv["wall_h"],
                                                       setup.cell_size, self.active_IA,
                                                       self.clock, self.obstacles,
                                                       self.interactables, self.door_pos))
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
                # TODO: das in eine Funktion:
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
        self.clock.draw(win)
        for i in self.active_IA:
            draw_interactables(win, self.win_copy, i)

        # characters
        self.chars["guy"].draw_char(win)
        for waiter in self.chars["waiter"]:
            waiter.draw_char(win)
        for guest in self.chars["guests"]:
            if guest.walk_in[0] == self.clock.h_m[0] and \
                    guest.walk_in[1] <= self.clock.h_m[1] or \
                    guest.walk_in[0] < self.clock.h_m[0]:
                guest.draw_char(win)

        #           Zeichnen - Balken und Text
        self.chars["guy"].draw_display(win, self.chars["guy"].drunkenness)  # Display guy
        for waiter in self.chars["waiter"]:
            waiter.draw_display(win, waiter.angryness)  # Display waiter
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
        self.halo_count += 1
        if self.halo_count >= 100:  # pi *30
            self.halo_count = 0
        self.filter_halo.set_alpha(round(math.sin((self.halo_count / 100) * math.pi) * 100))
        win.blit(self.filter_halo, (0, 0))

        self.draw_blits_specials(win, g)

    def draw_blits_specials(self, win, g):
        pass

    def init_main(self, win, setup, create_char):
        return {}

    def init_draw(self, win, setup, g):
        win.fill((0, 0, 0), (0, 0, setup.win_w, setup.win_h))
        win.blit(self.images.bg_walls, (self.sv["lvl_size"][0], self.sv["lvl_size"][1]))
        win.blit(self.images.img_ground, (self.sv["lvl_size"][0] + self.sv["wall_w"],
                                          self.sv["lvl_size"][1] + self.sv["wall_h"]))

        # get elements from init_main
        # ret_dict = self.init_main(win, setup, self.sv["enter_coord"], create_char)

        # Blit Objects and make a copy of the Screen
        for obst in self.obstacles:
            win.blit(obst.pic, (obst.x, obst.y))
        self.win_copy = win.copy()

        # Blit Interactables and Clock
        for inter in self.interactables:
            if inter.art == 'door' or inter.art == "radio":
                inter.draw_int(win, self.win_copy)
                self.active_IA.append(inter)
            else:
                inter.draw(win)
        self.clock.calc()
        self.clock.draw(win)
        self.active_IA.append(self.clock)

        # Create Raster
        Raster(win, self.sv["wall_w"], self.sv["wall_h"], self.sv["floor_pos"], self.sv["lvl_size"], setup.cell_size)
        # make Copy
        self.win_copy = win.copy()





        # adding level specific items
        self.init_draw_specials(win, setup, g)

        self.loaded = True

    def init_draw_specials(self, win, setup, g):
        pass

    def set_char_position(self, char, old_room):
        for door in filter(lambda x: isinstance(x, Door), self.interactables):
            if door.goto == old_room:
                char.x, char.y = self.sv["coords"]["w"][door.serv_pos[0]], self.sv["coords"]["h"][door.serv_pos[1]]

    def del_travel_char(self, win, char):
        dirtyrect = []
        for door in filter(lambda x: isinstance(x, Door), self.interactables):
            if door.goto == char.travel:
                del_pos = (self.sv["coords"]["w"][door.serv_pos[0]], self.sv["coords"]["h"][door.serv_pos[1]], 64, 64)        #   64 = cellsize!!!
                win.blit(self.win_copy, del_pos, del_pos)
                dirtyrect = [del_pos]
        return dirtyrect

    def reentry(self, setup, win):
        win.blit(self.win_copy, (0, 0))
        dr = [pygame.Rect(0, 0, setup.win_w, setup.win_h)]
        return dr


    def run_lvl(self, win, setup, g, travelling):

        dirtyrects = []
        run = True
        # Controls:
        if not travelling:
            run = controls_game(setup, self.chars, g, self.obstacles, self.interactables, self.sv)

        # Overblit with former State
        dirtyrects = dirtyrects + self.del_last_blit(win, setup, g)

        # Calculations
        dirtyrects = dirtyrects + self.movement_calculation(win, setup, g)

        # Blit actual State
        self.draw_blits(win, g)

        return run, dirtyrects
