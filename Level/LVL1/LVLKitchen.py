import pygame
from Scripts.Level.Level import Level

from Scripts.Util.LoadImages import ObstacleImages, LVLKitchenImages
from Scripts.Util.Functions import IncreaseI
from Scripts.Util.Obstacles import Door

from Scripts.Util.Clock import Clock

POS_GOALS = [(5, 5), (1, 1), (7, 7)]


class LVLKitchen(Level):
    def __init__(self, win, setup):
        images = LVLKitchenImages()
        lvl_size = images.bg_walls.get_size()
        ground_size = images.img_ground.get_size()

        super().__init__(win, setup, "lvl_kitchen", ObstacleImages(), lvl_size, ground_size)

        self.images = images
        self.width = lvl_size[0]
        self.height = lvl_size[1]
        self.clock = Clock(1, 1, 1)
        self.obstacles = []
        self.interactables = []
        self.music1 = pygame.mixer.music
        self.kerzen_list = []
        self.door_pos = []
        self.chairs = []
        self.halo_count = 0
        self.active_IA.append(self.clock)
        self.pos_goals = POS_GOALS


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
        _interactables = list()

        _interactables.append(
            Door(i.increase(), self.sv["coords"]["w"][4], self.sv["coords"]["h"][0],
                 self.sv["obst_images"].img_door[0].get_width(),
                 self.sv["obst_images"].img_door[0].get_height(),
                 180, self.sv["coords"], setup.cell_size, "lvl_main", "lvl_kitchen"))

        _door_pos = []
        for _i in _interactables:
            if _i.art == 'door':
                _door_pos.append(_i.serv_pos)

#        _obstacles.append(
#            Obstacle(i.increase(), "Walls_add", self.lvl_vars["images"].walls,
#                     self.sv["coords"]["w"][0], self.sv["coords"]["h"][0],
#                     self.lvl_vars["images"].walls.get_width(), self.lvl_vars["images"].walls.get_height()))

        self.obstacles = _obstacles
        self.interactables = _interactables
        self.door_pos = _door_pos
        self.filter_halo = filter_halo
        self.halo_count = 1

