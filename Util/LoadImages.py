import pygame


class ObstacleImages:
    def __init__(self):
        self.walls_add1 = pygame.image.load('../Graph/GUI/walls_add1.png')

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
        import os
        print(os.getcwd())
        self.bg = pygame.image.load('../Graph/GUI/walls_big.png').convert()
        self.img_ground = pygame.image.load('../Graph/GUI/floor_big.png').convert()
        self.inventory_pic = pygame.image.load('../Graph/GUI/inventory.png').convert()
        self.game_over = pygame.image.load('../Graph/GUI/gameOver.png').convert()