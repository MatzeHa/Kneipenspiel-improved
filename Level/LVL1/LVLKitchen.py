import pygame
from Scripts.Level.Level import Level

from Scripts.Util.LoadImages import ObstacleImages, LVLKitchenImages
from Scripts.Util.Functions import IncreaseI
from Scripts.Util.Obstacles import Door


class LVLKitchen(Level):
    def __init__(self, win, setup, clock):
        images = LVLKitchenImages()
        lvl_size = images.bg_walls.get_size()
        ground_size = images.img_ground.get_size()

        super().__init__(win, setup, "lvl_kitchen", ObstacleImages(), lvl_size, ground_size, (7, 0))

        self.images = images
        self.width = lvl_size[0]
        self.height = lvl_size[1]
        self.clock = clock
        self.obstacles = []
        self.interactables = []
        self.music1 = pygame.mixer.music
        self.kerzen_list = []
        self.door_pos = []
        self.chairs = []
        self.halo_count = 0
        self.filter_halo = pygame.Surface
        self.active_IA.append(clock)

    def init_main(self, win, setup, enter_coord, create_char=0):
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
        _interactables = list()

        _interactables.append(
            Door(i.increase(), self.sv["coord"]["w"][4], self.sv["coord"]["h"][0],
                 self.sv["obst_images"].img_door[0].get_width(),
                 self.sv["obst_images"].img_door[0].get_height(),
                 180, self.sv["coord"], setup.cell_size, "lvl_main", "lvl_kitchen"))

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
