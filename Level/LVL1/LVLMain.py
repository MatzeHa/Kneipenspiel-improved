import pygame
import random

from Scripts.Level.Level import Level

from Scripts.Util.LoadImages import ObstacleImages, LVLMainImages

from Scripts.Util.Clock import Clock
from Scripts.Util.Functions import IncreaseI

from Scripts.Entity.Player import Player
from Scripts.Entity.Waiter import Waiter
from Scripts.Entity.Guest import Guest


from Scripts.Util.Obstacles import Obstacle, Chalkboard, Kerze, KerzeWand, Radio, Barstool, Chair, Door, Stairs

pygame.init()


class LVLMain(Level):
    def __init__(self, win, setup):
        images = LVLMainImages()
        lvl_size = images.bg_walls.get_size()
        ground_size = images.img_ground.get_size()

        super().__init__(win, setup, "lvl_main", ObstacleImages(), lvl_size, ground_size, (3, 10))

        self.images = images
        self.width = lvl_size[0]
        self.height = lvl_size[1]
        self.clock = Clock
        self.obstacles = []
        self.interactables = []
        self.music1 = pygame.mixer.music
        self.radio = Radio
        self.kerzen_list = []
        self.door_pos = []
        self.chairs = []
        self.halo_count = 0
        self.filter_halo = pygame.Surface

    def init_main(self, win, setup, enter_coord, create_char=None):
        # Create Surfaces for Filters (Licht)
        filter_halo = pygame.Surface(
            (setup.win_w, setup.win_h))  # the size of your rect, ist für drunkenness filter
        filter_halo.set_colorkey((255, 255, 255))  # wichtig für maskieren
        filter_halo.fill((255, 255, 255))

        i = IncreaseI()

        # Fonts
        order_choose_font = pygame.font.SysFont('Courier', 33, True)
        order_choose_font.set_underline(True)

        # Obstacles und Interactables werden erstellt
        _obstacles = []
        _interactables = []

        _obstacles.append(
            Obstacle(i.increase(), "Walls_add", self.images.walls,
                     self.sv["coord"]["w"][21], self.sv["coord"]["h"][0],
                     self.images.walls.get_width(), self.images.walls.get_height()))
        _obstacles.append(
            Obstacle(i.increase(), "Theke", self.sv["obst_images"].img_bar, self.sv["coord"]["w"][3],
                     self.sv["coord"]["h"][0],
                     self.sv["obst_images"].img_bar.get_width(), self.sv["obst_images"].img_bar.get_height(), 0,
                     (2, 2)))
        _obstacles.append(
            Obstacle(i.increase(), "Schnapsregal", self.sv["obst_images"].img_schnapsregal, self.sv["coord"]["w"][0],
                     self.sv["coord"]["h"][0],
                     self.sv["obst_images"].img_schnapsregal.get_width(),
                     self.sv["obst_images"].img_schnapsregal.get_height()))

        # Tische und Stühle
        tisch_pos = {"tisch1": (9, 2), "tisch2": (10, 2), "tisch3": (17, 3), "tisch5": (18, 1), "tisch6": (22, 5),
                     "tisch7": (20, 7), "tisch9": (12, 9), "tisch10": (10, 8), "tisch11": (6, 10), "theke": (2, 4)}

        # Tisch 1
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_31, self.sv["coord"]["w"][6],
                     self.sv["coord"]["h"][2],
                     self.sv["obst_images"].img_table_31.get_width(),
                     self.sv["obst_images"].img_table_31.get_height(), 1, tisch_pos["tisch1"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][6], self.sv["coord"]["h"][1],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 1, tisch_pos["tisch1"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][7], self.sv["coord"]["h"][1],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 1, tisch_pos["tisch1"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][8], self.sv["coord"]["h"][1],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 1, tisch_pos["tisch1"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][6], self.sv["coord"]["h"][3],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 1, tisch_pos["tisch1"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][7], self.sv["coord"]["h"][3],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 1, tisch_pos["tisch1"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][8], self.sv["coord"]["h"][3],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 1, tisch_pos["tisch1"]))
        _interactables.append(
            Kerze(i.increase(), self.sv["coord"]["w"][7], self.sv["coord"]["h"][2],
                  self.sv["obst_images"].img_kerze[0].get_width(),
                  self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 0))

        # Tisch 2
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_11, self.sv["coord"]["w"][11],
                     self.sv["coord"]["h"][2],
                     self.sv["obst_images"].img_table_11.get_width(),
                     self.sv["obst_images"].img_table_11.get_height(),
                     2, tisch_pos["tisch2"]))
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_11, self.sv["coord"]["w"][12],
                     self.sv["coord"]["h"][2],
                     self.sv["obst_images"].img_table_11.get_width(),
                     self.sv["obst_images"].img_table_11.get_height(), 2, tisch_pos["tisch2"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][11], self.sv["coord"]["h"][1],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 2, tisch_pos["tisch2"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][11], self.sv["coord"]["h"][3],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 2, tisch_pos["tisch2"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][12], self.sv["coord"]["h"][1],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 2, tisch_pos["tisch2"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][12], self.sv["coord"]["h"][3],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 2, tisch_pos["tisch2"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][11], self.sv["coord"]["h"][2],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 1))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][12], self.sv["coord"]["h"][2],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 1))

        # Tisch 3
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_11, self.sv["coord"]["w"][16],
                     self.sv["coord"]["h"][2],
                     self.sv["obst_images"].img_table_11.get_width(),
                     self.sv["obst_images"].img_table_11.get_height(), 3, tisch_pos["tisch3"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][16], self.sv["coord"]["h"][1],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 3, tisch_pos["tisch3"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][16], self.sv["coord"]["h"][3],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 3, tisch_pos["tisch3"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][17], self.sv["coord"]["h"][2],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 3, tisch_pos["tisch3"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][16], self.sv["coord"]["h"][2],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 0))
        # Tisch 5
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_11, self.sv["coord"]["w"][19],
                     self.sv["coord"]["h"][0],
                     self.sv["obst_images"].img_table_11.get_width(),
                     self.sv["obst_images"].img_table_11.get_height(), 5, tisch_pos["tisch5"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][18], self.sv["coord"]["h"][0],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 5, tisch_pos["tisch5"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][19], self.sv["coord"]["h"][1],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 5, tisch_pos["tisch5"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][20], self.sv["coord"]["h"][0],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 5, tisch_pos["tisch5"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][19], self.sv["coord"]["h"][0],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 1))

        # Tisch 6
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_12, self.sv["coord"]["w"][22],
                     self.sv["coord"]["h"][3],
                     self.sv["obst_images"].img_table_12.get_width(),
                     self.sv["obst_images"].img_table_12.get_height(), 6, tisch_pos["tisch6"]))
        _interactables.append(Barstool(i.increase(), self.sv["coord"]["w"][21], self.sv["coord"]["h"][3],
                                       self.sv["obst_images"].img_barstool.get_width(),
                                       self.sv["obst_images"].img_barstool.get_height(), 270, 6, tisch_pos["tisch6"]))
        _interactables.append(Barstool(i.increase(), self.sv["coord"]["w"][21], self.sv["coord"]["h"][4],
                                       self.sv["obst_images"].img_barstool.get_width(),
                                       self.sv["obst_images"].img_barstool.get_height(), 270, 6, tisch_pos["tisch6"]))
        _interactables.append(Barstool(i.increase(), self.sv["coord"]["w"][23], self.sv["coord"]["h"][3],
                                       self.sv["obst_images"].img_barstool.get_width(),
                                       self.sv["obst_images"].img_barstool.get_height(), 90, 6, tisch_pos["tisch6"]))
        _interactables.append(Barstool(i.increase(), self.sv["coord"]["w"][23], self.sv["coord"]["h"][4],
                                       self.sv["obst_images"].img_barstool.get_width(),
                                       self.sv["obst_images"].img_barstool.get_height(), 90, 6, tisch_pos["tisch6"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][22], self.sv["coord"]["h"][3],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 0))

        # Tisch 7
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_13, self.sv["coord"]["w"][20],
                     self.sv["coord"]["h"][8],
                     self.sv["obst_images"].img_table_13.get_width(),
                     self.sv["obst_images"].img_table_13.get_height(), 7, tisch_pos["tisch7"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][19], self.sv["coord"]["h"][8],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 7, tisch_pos["tisch7"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][19], self.sv["coord"]["h"][9],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 7, tisch_pos["tisch7"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][19], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 7, tisch_pos["tisch7"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][21], self.sv["coord"]["h"][8],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 7, tisch_pos["tisch7"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][21], self.sv["coord"]["h"][9],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 7, tisch_pos["tisch7"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][21], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 7, tisch_pos["tisch7"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][20], self.sv["coord"]["h"][9],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 1))

        # Tisch 9
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_31, self.sv["coord"]["w"][13],
                     self.sv["coord"]["h"][9],
                     self.sv["obst_images"].img_table_31.get_width(),
                     self.sv["obst_images"].img_table_31.get_height(), 9, tisch_pos["tisch9"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][13], self.sv["coord"]["h"][8],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 9, tisch_pos["tisch9"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][14], self.sv["coord"]["h"][8],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 9, tisch_pos["tisch9"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][15], self.sv["coord"]["h"][8],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 9, tisch_pos["tisch9"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][13], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 9, tisch_pos["tisch9"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][14], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 9, tisch_pos["tisch9"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][15], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  0, 9, tisch_pos["tisch9"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][14], self.sv["coord"]["h"][9],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 0))

        # Tisch 10
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_13, self.sv["coord"]["w"][10],
                     self.sv["coord"]["h"][9],
                     self.sv["obst_images"].img_table_13.get_width(),
                     self.sv["obst_images"].img_table_13.get_height(), 10, tisch_pos["tisch10"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][9], self.sv["coord"]["h"][9],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 10, tisch_pos["tisch10"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][9], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 10, tisch_pos["tisch10"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][9], self.sv["coord"]["h"][11],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 10, tisch_pos["tisch10"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][11], self.sv["coord"]["h"][9],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 10, tisch_pos["tisch10"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][11], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 10, tisch_pos["tisch10"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][11], self.sv["coord"]["h"][11],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  90, 10, tisch_pos["tisch10"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][10], self.sv["coord"]["h"][10],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 1))

        # Tisch 11
        _obstacles.append(
            Obstacle(i.increase(), "Tisch", self.sv["obst_images"].img_table_11, self.sv["coord"]["w"][7],
                     self.sv["coord"]["h"][11],
                     self.sv["obst_images"].img_table_11.get_width(),
                     self.sv["obst_images"].img_table_11.get_height(), 11, tisch_pos["tisch11"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][6], self.sv["coord"]["h"][11],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  270, 11, tisch_pos["tisch11"]))
        _interactables.append(
            Chair(i.increase(), self.sv["coord"]["w"][7], self.sv["coord"]["h"][10],
                  self.sv["obst_images"].img_chair.get_width(),
                  self.sv["obst_images"].img_chair.get_height(),
                  180, 11, tisch_pos["tisch11"]))
        _interactables.append(Kerze(i.increase(), self.sv["coord"]["w"][7], self.sv["coord"]["h"][11],
                                    self.sv["obst_images"].img_kerze[0].get_width(),
                                    self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 0))

        # Thekenbestuhlung
        _interactables.append(
            Barstool(i.increase(), self.sv["coord"]["w"][6], self.sv["coord"]["h"][5],
                     self.sv["obst_images"].img_chair.get_width(),
                     self.sv["obst_images"].img_chair.get_height(),
                     90, 100, tisch_pos["theke"]))
        _interactables.append(
            Barstool(i.increase(), self.sv["coord"]["w"][6], self.sv["coord"]["h"][6],
                     self.sv["obst_images"].img_chair.get_width(),
                     self.sv["obst_images"].img_chair.get_height(),
                     90, 100, tisch_pos["theke"]))
        _interactables.append(
            Barstool(i.increase(), self.sv["coord"]["w"][5], self.sv["coord"]["h"][7],
                     self.sv["obst_images"].img_chair.get_width(),
                     self.sv["obst_images"].img_chair.get_height(),
                     0, 100, tisch_pos["theke"]))
        _interactables.append(
            Barstool(i.increase(), self.sv["coord"]["w"][4], self.sv["coord"]["h"][7],
                     self.sv["obst_images"].img_chair.get_width(),
                     self.sv["obst_images"].img_chair.get_height(),
                     0, 100, tisch_pos["theke"]))
        _interactables.append(
            Kerze(i.increase(), self.sv["coord"]["w"][5], self.sv["coord"]["h"][4],
                  self.sv["obst_images"].img_kerze[0].get_width(),
                  self.sv["obst_images"].img_kerze[0].get_height(), filter_halo, 1))

        # WandKerzen
        _interactables.append(
            KerzeWand(i.increase(),
                      self.sv["coord"]["w"][7],
                      self.sv["wall_h"] - 2 * setup.cell_size,
                      self.sv["obst_images"].img_kerze_wand.get_width(),
                      self.sv["obst_images"].img_kerze_wand.get_height(),
                      0,
                      filter_halo))
        _interactables.append(
            KerzeWand(i.increase(), self.sv["coord"]["w"][7],
                      setup.win_h - self.sv["wall_w"] + setup.cell_size,
                      self.sv["obst_images"].img_kerze_wand.get_width(),
                      self.sv["obst_images"].img_kerze_wand.get_height(), 180, filter_halo))
        _interactables.append(
            KerzeWand(i.increase(), self.sv["coord"]["w"][16], self.sv["wall_h"] - 2 * setup.cell_size,
                      self.sv["obst_images"].img_kerze_wand.get_width(),
                      self.sv["obst_images"].img_kerze_wand.get_height(), 0, filter_halo))
        _interactables.append(
            KerzeWand(i.increase(), self.sv["coord"]["w"][16],
                      setup.win_h - self.sv["wall_w"] + setup.cell_size,
                      self.sv["obst_images"].img_kerze_wand.get_width(),
                      self.sv["obst_images"].img_kerze_wand.get_height(), 180, filter_halo))
        _interactables.append(KerzeWand(i.increase(), self.sv["coord"]["w"][22], self.sv["coord"]["h"][1],
                                        self.sv["obst_images"].img_kerze_wand.get_width(),
                                        self.sv["obst_images"].img_kerze_wand.get_height(), 0, filter_halo))

        _interactables.append(
            Chalkboard(i.increase(), self.sv["coord"]["w"][11], setup.win_h - self.sv["wall_h"],
                       self.sv["obst_images"].img_chalkboard.get_width(),
                       self.sv["obst_images"].img_chalkboard.get_height(), 180))
        i = IncreaseI()
        _interactables.append(
            Door(i.increase(), self.sv["coord"]["w"][0], self.sv["coord"]["h"][12],
                 self.sv["obst_images"].img_door[0].get_width(),
                 self.sv["obst_images"].img_door[0].get_height(),
                 0, self.sv["coord"], setup.cell_size, "lvl_kitchen"))
        _interactables.append(
            Door(i.increase(), self.sv["coord"]["w"][25], self.sv["coord"]["h"][3],
                 self.sv["obst_images"].img_door[0].get_width(),
                 self.sv["obst_images"].img_door[0].get_height(),
                 90, self.sv["coord"], setup.cell_size, "lvl_outside"))
        _door_pos = []

        _interactables.append(
            Stairs(i.increase(), self.sv["coord"]["w"][13], self.sv["coord"]["h"][0],
                   self.sv["obst_images"].img_stairs.get_width(),
                   self.sv["obst_images"].img_stairs.get_height(),
                   90, self.sv["coord"][self.sv["max_coord"]], setup.cell_size))
        for _i in _interactables:
            if _i.art == 'door' or _i.art == 'stairs':
                _door_pos.append(_i.serv_pos)

        _radio = Radio(i.increase(), self.sv["coord"]["w"][1], self.sv["coord"]["h"][0],
                       self.sv["obst_images"].img_radio[0].get_width(),
                       self.sv["obst_images"].img_radio[0].get_height())
        _interactables.append(_radio)

        _chairs = []
        _kerzen_list = []
        for _i in _interactables:
            if _i.art == 'chair':
                _chairs.append(_i)
            if _i.art == 'kerze':
                _kerzen_list.append(_i)
        random.shuffle(_chairs)

        _clock = Clock(i.increase(), 50, 500)

        _guy = Player(self.sv["coord"]["w"][enter_coord[0]], self.sv["coord"]["h"][enter_coord[1]], setup.cell_size,
                      setup.cell_size, True, create_char.new_tilemap, 64 / 8)

        _waiter = [
            Waiter(self.sv["coord"]["w"][2], self.sv["coord"]["h"][2], setup.cell_size, setup.cell_size,
                   _obstacles, True,
                   create_char.create_tilemap(win))]
        _guests = []
        for _i in range(0, 20):
            vel = 8
            guest = Guest(self.sv["coord"]["w"][24], self.sv["coord"]["h"][6], setup.cell_size,
                          setup.cell_size, vel, _chairs.pop(),
                          (random.randint(0, 0), random.randint(0, 20)), False)
            _guests.append(guest)

        _halo_count = 1

        return_dict = {"obstacles": _obstacles,
                       "interactables": _interactables,
                       "door_pos": _door_pos,
                       "radio": _radio,
                       "chairs": _chairs,
                       "kerzen_list": _kerzen_list,
                       "clock": _clock,
                       "guy": _guy,
                       "waiter": _waiter,
                       "guests": _guests,
                       "halo_count": _halo_count,
                       "filter_halo": filter_halo}

        return return_dict

    def init_draw_specials(self, win, setup, g, create_char, ret_dict):
        for inter in ret_dict["interactables"]:
            if inter.art == ret_dict["radio"]:
                inter.draw_int(win, self.sv["win_copy"])
                self.active_IA.append(inter)
        g.dialog_menue.chars[0] = ret_dict["guy"]

        self.chars["guy"] = ret_dict["guy"]
        self.chars["waiter"] = ret_dict["waiter"]
        self.chars["guests"] = ret_dict["guests"]
        self.radio = ret_dict["radio"]
        self.kerzen_list = ret_dict["kerzen_list"]
        self.chairs = ret_dict["chairs"]
        self.halo_count = ret_dict["halo_count"]
        self.clock = ret_dict["clock"]
        music1 = pygame.mixer.music.load('../Sound/BlueSkies.mp3')
        self.music1 = music1

    def del_lvl_specials(self, win):
        dirtyrects = list()
        dirtyrects.append(self.radio.del_blit(win, self.win_copy))
        for i in self.kerzen_list:  # Kerzen löschen
            dirtyrects.append(i.repaint(win, self.win_copy))
        return dirtyrects
