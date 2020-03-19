import pygame


class ObstacleImages:
    def __init__(self):

        self.img_door = [pygame.image.load('../Graph/Inter/door/door0.png'),
                         pygame.image.load('../Graph/Inter/door/door1.png'),
                         pygame.image.load('../Graph/Inter/door/door2.png'),
                         pygame.image.load('../Graph/Inter/door/door3.png'),
                         pygame.image.load('../Graph/Inter/door/door4.png'),
                         pygame.image.load('../Graph/Inter/door/door5.png')]

        self.img_kerze = [pygame.image.load('../Graph/Inter/kerze_gelb.png'),
                          pygame.image.load('../Graph/Inter/kerze_rot.png')]
        self.img_kerze_wand = pygame.image.load('../Graph/Inter/kerze_wand.png')
        # Halo = pygame.image.load('../Graph/Halo.png')

        self.img_radio = [pygame.image.load('../Graph/Inter/radio/radio0.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio1.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio2.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio3.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio4.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio5.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio6.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio7.png'),
                          pygame.image.load('../Graph/Inter/radio/Radio8.png')]

        self.img_bar = pygame.image.load('../Graph/Obst/Bar_3_7.png')
        # Tisch_22 = pygame.image.load('../Graph/Obst/tisch.png')
        self.img_table_31 = pygame.image.load('../Graph/Obst/tisch31.png')
        self.img_table_21 = pygame.image.load('../Graph/Obst/tisch21.png')
        self.img_table_13 = pygame.image.load('../Graph/Obst/tisch13.png')
        self.img_table_12 = pygame.image.load('../Graph/Obst/tisch12.png')
        self.img_table_11 = pygame.image.load('../Graph/Obst/tisch11.png')
        self.img_schnapsregal = pygame.image.load('../Graph/Obst/Schnapsregal.png')

        self.img_chair = pygame.image.load('../Graph/Inter/chair.png')
        self.img_barstool = pygame.image.load('../Graph/Inter/barstool.png')
        self.img_stairs = pygame.image.load('../Graph/Inter/treppe.png')

        self.img_chalkboard = pygame.image.load('../Graph/Inter/chalkboard.png')

        self.rotDict = {0: 0, 90: 3, 180: 2, 270: 1}
        self.img_ground = pygame.image.load('../Graph/GUI/floor_big.png')


class LVLMainImages:
    def __init__(self):
        self.bg = pygame.image.load('../Graph/GUI/walls_big.png').convert()
        self.img_ground = pygame.image.load('../Graph/GUI/floor_big.png').convert()
        self.walls = pygame.image.load('../Graph/GUI/walls_add1.png')
        self.inventory_pic = pygame.image.load('../Graph/GUI/inventory.png').convert()
        self.game_over = pygame.image.load('../Graph/GUI/gameOver.png').convert()


class LVLKitchenImages:
    def __init__(self):
        self.bg = pygame.image.load('../Graph/GUI/kitchen_walls.png').convert()
        self.img_ground = pygame.image.load("../Graph/GUI/kitchen_floor.png").convert()
        self.walls = pygame.image.load('../Graph/GUI/kitchen_walls.png').convert()

class CharCreationImages:
    def __init__(self):
        from Scripts.Util.ScaleImage import scale_image
        img_tilemap_guy = pygame.image.load("../Graph/chars/guy/guy_BW.png")

        self.img_guy_BW = {"head": img_tilemap_guy.subsurface((0, 0, 64, 64)),
                           "shirt": img_tilemap_guy.subsurface((64, 0, 64, 64)),
                           "pants_sit": img_tilemap_guy.subsurface((128, 0, 64, 64)),
                           "shoes_sit": img_tilemap_guy.subsurface((192, 0, 64, 64)),
                           "shoes_walk0": img_tilemap_guy.subsurface((0, 64, 64, 64)),
                           "shoes_walk1": img_tilemap_guy.subsurface((64, 64, 64, 64)),
                           "shoes_walk2": img_tilemap_guy.subsurface((128, 64, 64, 64)),
                           "shoes_walk3": img_tilemap_guy.subsurface((192, 64, 64, 64)),
                           "hands_sit": img_tilemap_guy.subsurface((0, 128, 64, 64)),
                           "hands_walk1": img_tilemap_guy.subsurface((64, 128, 64, 64)),
                           "hands_walk2": img_tilemap_guy.subsurface((128, 128, 64, 64)),
                           "hands_walk3": img_tilemap_guy.subsurface((192, 128, 64, 64)),
                           "pants_walk2": img_tilemap_guy.subsurface((128, 192, 64, 64)),
                           "pants_walk3": img_tilemap_guy.subsurface((192, 192, 64, 64))
                           }

        self.img_head_bw, _ = scale_image(self.img_guy_BW["head"], 300)
        self.img_head = self.img_head_bw.copy()
        self.img_shirt_bw, _ = scale_image(self.img_guy_BW["shirt"], 300)
        self.img_shirt = self.img_shirt_bw.copy()
        self.img_pants_bw, _ = scale_image(self.img_guy_BW["pants_sit"], 300)
        self.img_pants = self.img_pants_bw.copy()
        self.img_shoes_bw, _ = scale_image(self.img_guy_BW["shoes_sit"], 300)
        self.img_shoes = self.img_shoes_bw.copy()
        self.img_hands_bw, _ = scale_image(self.img_guy_BW["hands_sit"], 300)
        self.img_hands = self.img_hands_bw.copy()
        self.img_w, self.img_h = self.img_head.get_size()
