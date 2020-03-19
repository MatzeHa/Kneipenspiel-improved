import pygame
from Scripts.Level.Level import Level

from Scripts.Util.LoadImages import ObstacleImages, LVLMainImages



class LVLKitchen:
    def __init__(self, win, setup):
        Level.__init__(self, win, setup, "main", LVLMainImages(), ObstacleImages(), 150, 150)

        self.lvl_vars = {"clock": None,
                         "obstacles": [],
                         "interactables": [],
                         "music1": None,
                         "radio": None,
                         "kerzen_list": [],
                         "door_pos": [],
                         "chairs": [],
                         "halo_count": 0,
                         "filter_halo": None}

    def run_lvl(self, win, setup, g):
        print("KÜCHE!")
        return True, pygame.Rect(0, 0, 500, 500)