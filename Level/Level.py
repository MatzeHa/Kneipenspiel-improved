from Scripts.Util.Functions import get_max_coord
from Scripts.Util.Functions import Raster


class Level:
    def __init__(self, win, setup, name, images, obst_images, wall_w, wall_h):
        self.name = name
        self.sv = {"images": images,
                   "obst_images": obst_images,
                   "wall_w": wall_w,
                   "wall_h": wall_h,
                   "cell_size": setup.cell_size,
                   "coord": setup.coord,
                   "max_coord": get_max_coord(setup.coord),
                   "raster": Raster(win, setup.wall_w, setup.wall_h, setup.cell_size)
                   }

        self.win_copy = win.copy()
        self.win_copy_change_mode = win.copy()
        self.active_IA = []         # active Interactables
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
            if guest.walk_in[0] == self.lvl_vars["clock"].h_m[0] and guest.walk_in[1] <= self.lvl_vars["clock"].h_m[1] or guest.walk_in[0] < \
                    self.lvl_vars["clock"].h_m[0]:
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
