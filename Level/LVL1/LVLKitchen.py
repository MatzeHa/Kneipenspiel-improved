import pygame
from Scripts.Level.Level import Level

from Scripts.Util.LoadImages import ObstacleImages, LVLKitchenImages
from Scripts.Util.Functions import IncreaseI
from Scripts.Util.Obstacles import Obstacle, Door


class LVLKitchen(Level):
    def __init__(self, win, setup, clock):
        images = LVLKitchenImages()
        lvl_size = images.bg_walls.get_size()
        ground_size = images.img_ground.get_size()

        super().__init__(win, setup, "lvl_kitchen", ObstacleImages(), lvl_size, ground_size, (10, 1))

        self.lvl_vars = {"images": images,
                         "width": lvl_size[0],
                         "height": lvl_size[1],
                         "clock": clock,
                         "obstacles": [],
                         "interactables": [],
                         "music1": None,
                         "radio": None,
                         "kerzen_list": [],
                         "door_pos": [],
                         "chairs": [],
                         "halo_count": 0,
                         "filter_halo": None}
        self.active_IA.append(clock)

    def init_main(self, win, setup, create_char=0):
        # self.chars
        # Create Surfaces for Filters (Licht)
        filter_halo = pygame.Surface((setup.win_w, setup.win_h))  # the size of your rect, ist für drunkenness filter
        filter_halo.set_colorkey((255, 255, 255))  # wichtig für maskieren
        filter_halo.fill((255, 255, 255))

        i = IncreaseI()

        # Fonts
        order_choose_font = pygame.font.SysFont('Courier', 33, True)
        order_choose_font.set_underline(True)

        # Obstacles und Interactables werden erstellt
        _obstacles = []
        _interactables = []

        _interactables.append(
            Door(i.increase(), self.sv["coord"]["w"][0], self.sv["coord"]["h"][7],
                 self.sv["obst_images"].img_door[0].get_width(),
                 self.sv["obst_images"].img_door[0].get_height(),
                 180, self.sv["coord"], setup.cell_size, "schachtel_oben"))

        _door_pos = []
        for _i in _interactables:
            if _i.art == 'door':
                _door_pos.append(_i.serv_pos)

#        _obstacles.append(
#            Obstacle(i.increase(), "Walls_add", self.lvl_vars["images"].walls,
#                     self.sv["coord"]["w"][0], self.sv["coord"]["h"][0],
#                     self.lvl_vars["images"].walls.get_width(), self.lvl_vars["images"].walls.get_height()))

        return_dict = {"obstacles": _obstacles,
                       "interactables": _interactables,
                       "door_pos": _door_pos,
                       "filter_halo": filter_halo}
        return return_dict