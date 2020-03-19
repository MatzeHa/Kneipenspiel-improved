import pygame
import random
import math

from Scripts.Level.Level import Level

from Scripts.Util.LoadImages import ObstacleImages, LVLMainImages

from Scripts.Util.Functions import get_max_coord, Raster, global_var, draw_interactables
from Scripts.Util.Clock import Clock
from Scripts.Util.Controls import controls_game
from Scripts.Util.Functions import IncreaseI

from Scripts.Entity.Player import Player
from Scripts.Entity.Waiter import Waiter
from Scripts.Entity.Guest import Guest
from Scripts.GameModes.Order import OrderMenue
from Scripts.GameModes.Dialog import DialogMenue


from Scripts.Util.Obstacles import Obstacle, Chalkboard, Kerze, KerzeWand, Radio, Barstool, Chair, Door, Stairs

pygame.init()


class LVLMain(Level):
    def __init__(self, win, setup):
        Level.__init__(self, win, setup, "main", LVLMainImages(), ObstacleImages(), 150, 150)

        self.lvl_vars = {"clock": Clock,
                         "obstacles": [],
                         "interactables": [],
                         "music1": pygame.mixer.music,
                         "radio": Radio,
                         "kerzen_list": [],
                         "door_pos": [],
                         "chairs": [],
                         "halo_count": 0,
                         "filter_halo": pygame.Surface}

    def init_main(self, win, setup, create_char):
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
            Obstacle(i.increase(), "Walls_add", self.sv["obst_images"].walls_add1, self.sv["coord"]["w"][21],
                     self.sv["coord"]["h"][0],
                     self.sv["obst_images"].walls_add1.get_width(), self.sv["obst_images"].walls_add1.get_height()))
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
                      self.sv["wall_h"] - 2 * self.sv["cell_size"],
                      self.sv["obst_images"].img_kerze_wand.get_width(),
                      self.sv["obst_images"].img_kerze_wand.get_height(),
                      0,
                      filter_halo))
        _interactables.append(
            KerzeWand(i.increase(), self.sv["coord"]["w"][7],
                      setup.win_h - self.sv["wall_w"] + self.sv["cell_size"],
                      self.sv["obst_images"].img_kerze_wand.get_width(),
                      self.sv["obst_images"].img_kerze_wand.get_height(), 180, filter_halo))
        _interactables.append(
            KerzeWand(i.increase(), self.sv["coord"]["w"][16], self.sv["wall_h"] - 2 * self.sv["cell_size"],
                      self.sv["obst_images"].img_kerze_wand.get_width(),
                      self.sv["obst_images"].img_kerze_wand.get_height(), 0, filter_halo))
        _interactables.append(
            KerzeWand(i.increase(), self.sv["coord"]["w"][16],
                      setup.win_h - self.sv["wall_w"] + self.sv["cell_size"],
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
                 0, self.sv["coord"], self.sv["cell_size"], "lvl_kitchen"))
        _interactables.append(
            Door(i.increase(), self.sv["coord"]["w"][25], self.sv["coord"]["h"][3],
                 self.sv["obst_images"].img_door[0].get_width(),
                 self.sv["obst_images"].img_door[0].get_height(),
                 90, self.sv["coord"], self.sv["cell_size"], "lvl_outside"))
        _door_pos = []

        _interactables.append(
            Stairs(i.increase(), self.sv["coord"]["w"][13], self.sv["coord"]["h"][0],
                   self.sv["obst_images"].img_stairs.get_width(),
                   self.sv["obst_images"].img_stairs.get_height(),
                   90, self.sv["coord"][self.sv["max_coord"]], self.sv["cell_size"]))
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

        _guy = Player(self.sv["coord"]["w"][8], self.sv["coord"]["h"][4], self.sv["cell_size"],
                      self.sv["cell_size"], True, create_char.new_tilemap, 64 / 8)
        _waiter = [
            Waiter(self.sv["coord"]["w"][2], self.sv["coord"]["h"][2], self.sv["cell_size"], self.sv["cell_size"],
                   _obstacles, True,
                   create_char.create_tilemap(win))]
        _guests = []
        for _i in range(0, 10):
            vel = 8
            guest = Guest(self.sv["coord"]["w"][24], self.sv["coord"]["h"][6], self.sv["cell_size"],
                          self.sv["cell_size"], vel, _chairs.pop(),
                          (random.randint(0, 0), random.randint(0, 20)), False)
            _guests.append(guest)


        _halo_count = 1

        return _obstacles, _interactables, _door_pos, _radio, _chairs, _kerzen_list, _clock, _guy, _waiter, \
            _guests, _halo_count, filter_halo

    def init_draw(self, win, setup, create_char, g):



        win.blit(self.sv["images"].bg, (0, 0))
        win.blit(self.sv["images"].img_ground, (self.sv["wall_w"], self.sv["wall_h"]))

        obstacles, interactables, door_pos, radio, chairs, kerzen_list, clock, guy, waiter, \
            guests, halo_count, filter_halo = self.init_main(win, setup, create_char)

        for obst in obstacles:
            win.blit(obst.pic, (obst.x, obst.y))

        self.sv["win_copy"] = win.copy()

        for inter in interactables:
            if inter.art == 'door' or inter.art == 'radio':
                inter.draw_int(win, self.sv["win_copy"])
                self.active_IA.append(inter)
            else:
                inter.draw(win)

        clock.calc()
        clock.draw(win)
        self.active_IA.append(clock)

        raster = Raster(win, self.sv["wall_w"], self.sv["wall_h"], self.sv["cell_size"])
        # raster.draw(win)
        self.sv["win_copy"] = win.copy()

        self.chars["waiter"] = waiter
        self.chars["guests"] = guests
        self.lvl_vars["obstacles"] = obstacles
        self.lvl_vars["interactables"] = interactables
        self.lvl_vars["door_pos"] = door_pos
        self.lvl_vars["raster"] = raster
        self.lvl_vars["clock"] = clock


        music1 = pygame.mixer.music.load('../Sound/BlueSkies.mp3')

        self.chars["guy"] = guy

        self.lvl_vars["music1"] = music1
        self.lvl_vars["radio"] = radio
        self.lvl_vars["kerzen_list"] = kerzen_list
        self.lvl_vars["chairs"] = chairs
        self.lvl_vars["halo_count"] = halo_count
        self.lvl_vars["filter_halo"] = filter_halo

        g.dialog_menue.chars[0] = guy

    def draw_blits(self, win, g):

        _dirtyrects = []
        self.lvl_vars["clock"].draw(win)
        for i in self.active_IA:
            draw_interactables(win, self.sv["win_copy"], i)

        # characters
        self.chars["guy"].draw_char(win)
        self.chars["waiter"][0].draw_char(win)
        for guest in self.chars["guests"]:
            if guest.walk_in[0] == self.lvl_vars["clock"].h_m[0] and \
                    guest.walk_in[1] <= self.lvl_vars["clock"].h_m[1] or \
                    guest.walk_in[0] < self.lvl_vars["clock"].h_m[0]:
                guest.draw_char(win)

        #           Zeichnen - Balken und Text
        self.chars["guy"].draw_display(win, self.chars["guy"].drunkenness)  # Display guy
        self.chars["waiter"][0].draw_display(win, self.chars["waiter"][0].angryness)  # Display guy
        for i in self.chars["guests"]:
            if i.inside:
                _dirtyrects.append(i.draw_display(win, i.drunkenness))  # Display Gäste

        # Zeige Text an
        if self.chars["guy"].text_count < 50:
            _dirtyrects.append(self.chars["guy"].talk(win))
        if self.chars["waiter"][0].text_count < 50:
            _dirtyrects.append(self.chars["waiter"][0].talk(win))
        for i in self.chars["guests"]:
            if i.text_count < 50:
                _dirtyrects.append(i.talk(win))

        # Filter für Lichteffekte
        self.lvl_vars["halo_count"] += 1
        if self.lvl_vars["halo_count"] >= 100:  # pi *30
            self.lvl_vars["halo_count"] = 0
        self.lvl_vars["filter_halo"].set_alpha(round(math.sin((self.lvl_vars["halo_count"] / 100) * math.pi) * 100))
        win.blit(self.lvl_vars["filter_halo"], (0, 0))


    def del_last_blit(self, win, setup, g):
        dirtyrects = []
        # wenn OrderMenue aufgemacht wird, wird eine Kopie des gesamten Bildes gespeichert
        if self.chars["guy"].orderAction == 5:
            # self.sv["win_copy"]
            self.chars["guy"].orderAction = 6

        # wenn OrderMenue geschlossen wird, wird das Bild mit  der Kopie üüberblittet
        elif self.chars["guy"].orderAction == 7:
            win.blit(self.sv["win_copy"], (0, 0))
            dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))
            self.chars["guy"].orderAction = 8

        # wenn Dialog Menue aufgemacht wird, wird eine Kopie des gesamten Bildes gespeichert
        elif self.chars["guy"].talk_action == 1:
            self.sv["win_copy_change_mode"] = win.copy()
            g.dialog_menue.active = True
            self.chars["guy"].talk_action = 2

        # überblitten mit alter Kopie
        elif self.chars["guy"].talk_action == 2:
            win.blit(self.sv["win_copy"], (0, 0))
            dirtyrects.append(pygame.Rect(0, 0, setup.win_w, setup.win_h))

        # Wenn Normales In-Game Window angezeigt wird, soll alles, was sich bewegen kann, ( auch halos )
        # wieder mit Kopie ohne bewegliche sachen überblittet werden.
        else:
            dirtyrects.append(self.lvl_vars["radio"].del_blit(win, self.sv["win_copy"]))
            for i in self.lvl_vars["kerzen_list"]:  # Kerzen löschen
                dirtyrects.append(i.repaint(win, self.sv["win_copy"]))
            dirtyrects.append(self.chars["guy"].del_blit(win, self.sv["win_copy"]))  # guy
            dirtyrects.append(self.chars["guy"].del_display(win, self.sv["win_copy"]))  # Display guy
            if self.chars["guy"].text_count < 51:  # Textzeile wieder überblitten
                dirtyrects.append(self.chars["guy"].del_text(win, self.sv["win_copy"]))

            dirtyrects.append(self.chars["waiter"][0].del_blit(win, self.sv["win_copy"]))  # Waiter
            dirtyrects.append(self.chars["waiter"][0].del_display(win, self.sv["win_copy"]))  # Display Waiter
            if self.chars["waiter"][0].text_count < 51:  # Textzeile wieder überblitten
                dirtyrects.append(self.chars["waiter"][0].del_text(win, self.sv["win_copy"]))

            for i in self.chars["guests"]:
                dirtyrects.append(i.del_blit(win, self.sv["win_copy"]))  # Guests
                dirtyrects.append(i.del_display(win, self.sv["win_copy"]))  # Display Waiter
                if i.text_count < 51:  # Textzeile wieder überblitten
                    dirtyrects.append(i.del_text(win, self.sv["win_copy"]))
        #        # Inventar offen:
        #        if inventory_active:
        #            invent.draw(win, inventory_pic, guy.inventory)

        return dirtyrects

    def run_lvl(self, win, setup, g):

        print("MAIN-LEVEL RUN")


        # TODO: HIER weitermachen! Küche ienbauen, setup.wall_size anpassen!!!
        # TODO: guy.room abfragen!!!
        dirtyrects = []

        # Controls:
        run = controls_game(setup, self.chars, g, self.lvl_vars["obstacles"], self.lvl_vars["interactables"])

        # Overblit with former State
        dirtyrects = dirtyrects + self.del_last_blit(win, setup, g)

        # Calculations
        dirtyrects = dirtyrects + self.movement_calculation(win, setup, g)

        # Blit actual State
        self.draw_blits(win, g)

        return run, dirtyrects

