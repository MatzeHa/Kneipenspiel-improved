import pygame

from Scripts.Util.QuitGame import quit_game
from Scripts.Util.ScaleImage import scale_image
from Scripts.Util.LoadImages import CharCreationImages

pygame.init()

pygame.display.set_caption("Matzes Kneipenspiel - Charaktererstellung", "MK")


class CreateChar:
    def __init__(self):
        cci = CharCreationImages()

        self.creation_active = True
        self.sv = {"images": cci.img_guy_BW,
                   "tm_images": {0: [cci.img_head, 0, get_boundary(cci.img_head)],  # tilemap-images
                                 1: [cci.img_shirt, 0, get_boundary(cci.img_shirt)],
                                 2: [cci.img_pants, 0, get_boundary(cci.img_pants)],
                                 3: [cci.img_shoes, 0, get_boundary(cci.img_shoes)],
                                 4: [cci.img_hands, 0, get_boundary(cci.img_hands)]
                                 },
                   "img_w": cci.img_w,
                   "img_h": cci.img_h
                   }

        self.timer_clock = pygame.time.Clock()

        self.bw_list = [cci.img_head_bw, cci.img_shirt_bw, cci.img_pants_bw, cci.img_shoes_bw,
                        cci.img_hands_bw]

        self.cursor = 0
        self.new_tilemap = None

    def start_creation(self, win, setup):
        self.init_blit(win, setup)
        self.run(win, setup)
        self.new_tilemap = self.create_tilemap(win)

    def init_blit(self, win, setup):
        self.draw_spectre(win, setup)
        self.draw_all(win, setup)
        setup.win_copy = win.copy()

    def run(self, win, setup):
        run = True
        while run:
            change_color_ok = False
            self.del_cursor(win, setup)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    quit_game()
                if keys[pygame.K_UP]:
                    self.cursor_up()
                if keys[pygame.K_DOWN]:
                    self.cursor_down()
            if keys[pygame.K_LEFT]:
                self.cursor_left()
            if keys[pygame.K_RIGHT]:
                self.cursor_right()
            if keys[pygame.K_e]:
                change_color_ok = True
            if keys[pygame.K_RETURN]:
                run = False
            self.draw_spectre(win, setup)
            if change_color_ok:
                self.change_color(self.cursor)
            self.draw_all(win, setup)
            self.draw_cursor(win, setup)

            self.timer_clock.tick(30)
            # print("FPS: ", self.timer_clock.get_fps())
            pygame.display.update()

    def create_tilemap(self, win):
        from random import randint
        tilemap = pygame.Surface([512, 512], pygame.SRCALPHA, 32)
        tilemap = tilemap.convert_alpha()

        if self.creation_active:
            col_head = get_color(self.sv["tm_images"][0][1])
            col_shirt = get_color(self.sv["tm_images"][1][1])
            col_shoes = get_color(self.sv["tm_images"][3][1])
            col_hands = get_color(self.sv["tm_images"][4][1])
            col_pants = get_color(self.sv["tm_images"][2][1])
        else:
            col_head = get_color(randint(0, 100))
            col_shirt = get_color(randint(0, 100))
            col_shoes = get_color(randint(0, 100))
            col_hands = get_color(randint(0, 100))
            col_pants = get_color(randint(0, 100))

        head = fill(self.sv["images"]["head"], col_head)
        shirt = fill(self.sv["images"]["shirt"], col_shirt)

        walk0_shoes = fill(self.sv["images"]["shoes_walk0"], col_shoes)

        walk1_hands = fill(self.sv["images"]["hands_walk1"], col_hands)
        walk1_shoes = fill(self.sv["images"]["shoes_walk1"], col_shoes)

        walk2_hands = fill(self.sv["images"]["hands_walk2"], col_hands)
        walk2_shoes = fill(self.sv["images"]["shoes_walk2"], col_shoes)
        walk2_pants = fill(self.sv["images"]["pants_walk2"], col_pants)

        walk3_hands = fill(self.sv["images"]["hands_walk3"], col_hands)
        walk3_shoes = fill(self.sv["images"]["shoes_walk3"], col_shoes)
        walk3_pants = fill(self.sv["images"]["pants_walk3"], col_pants)

        sit_hands = fill(self.sv["images"]["hands_sit"], col_hands)
        sit_shoes = fill(self.sv["images"]["shoes_sit"], col_shoes)
        sit_pants = fill(self.sv["images"]["pants_sit"], col_pants)

        # walk0
        tilemap.blit(walk0_shoes, (0, 0))
        tilemap.blit(shirt, (0, 0))
        tilemap.blit(head, (0, 0))

        # walk1
        tilemap.blit(walk1_hands, (64, 0))
        tilemap.blit(walk1_shoes, (64, 0))
        tilemap.blit(shirt, (64, 0))
        tilemap.blit(head, (64, 0))

        # walk2
        tilemap.blit(walk2_hands, (128, 0))
        tilemap.blit(walk2_shoes, (128, 0))
        tilemap.blit(walk2_pants, (128, 0))
        tilemap.blit(shirt, (128, 0))
        tilemap.blit(head, (128, 0))

        # walk3
        tilemap.blit(walk3_hands, (192, 0))
        tilemap.blit(walk3_shoes, (192, 0))
        tilemap.blit(walk3_pants, (192, 0))
        tilemap.blit(shirt, (192, 0))
        tilemap.blit(head, (192, 0))

        # walk4
        tilemap.blit(pygame.transform.flip(walk1_hands, 1, 0), (256, 0))
        tilemap.blit(pygame.transform.flip(walk1_shoes, 1, 0), (256, 0))
        tilemap.blit(pygame.transform.flip(shirt, 1, 0), (256, 0))
        tilemap.blit(pygame.transform.flip(head, 1, 0), (256, 0))

        # walk5
        tilemap.blit(pygame.transform.flip(walk2_hands, 1, 0), (320, 0))
        tilemap.blit(pygame.transform.flip(walk2_shoes, 1, 0), (320, 0))
        tilemap.blit(pygame.transform.flip(walk2_pants, 1, 0), (320, 0))
        tilemap.blit(pygame.transform.flip(shirt, 1, 0), (320, 0))
        tilemap.blit(pygame.transform.flip(head, 1, 0), (320, 0))

        # walk6
        tilemap.blit(pygame.transform.flip(walk3_hands, 1, 0), (384, 0))
        tilemap.blit(pygame.transform.flip(walk3_shoes, 1, 0), (384, 0))
        tilemap.blit(pygame.transform.flip(walk3_pants, 1, 0), (384, 0))
        tilemap.blit(pygame.transform.flip(shirt, 1, 0), (384, 0))
        tilemap.blit(pygame.transform.flip(head, 1, 0), (384, 0))

        # sit
        tilemap.blit(pygame.transform.flip(sit_hands, 1, 0), (448, 0))
        tilemap.blit(pygame.transform.flip(sit_shoes, 1, 0), (448, 0))
        tilemap.blit(pygame.transform.flip(sit_pants, 1, 0), (448, 0))
        tilemap.blit(pygame.transform.flip(shirt, 1, 0), (448, 0))
        tilemap.blit(pygame.transform.flip(head, 1, 0), (448, 0))

        win.blit(tilemap, (0, 0))

        self.creation_active = False
        return tilemap

    def change_color(self, cursor):
        img = self.bw_list[cursor]
        col = get_color(self.sv["tm_images"][cursor][1])
        self.sv["tm_images"][cursor][0] = fill(img, col)
        return self.sv["tm_images"][cursor][0]

    def draw_all(self, win, setup):
        win.blit(self.sv["tm_images"][4][0],
                 (setup.win_w / 2 - self.sv["img_w"] / 2, setup.win_h / 2 - self.sv["img_h"] / 2))
        win.blit(self.sv["tm_images"][3][0],
                 (setup.win_w / 2 - self.sv["img_w"] / 2, setup.win_h / 2 - self.sv["img_h"] / 2))
        win.blit(self.sv["tm_images"][2][0],
                 (setup.win_w / 2 - self.sv["img_w"] / 2, setup.win_h / 2 - self.sv["img_h"] / 2))
        win.blit(self.sv["tm_images"][1][0],
                 (setup.win_w / 2 - self.sv["img_w"] / 2, setup.win_h / 2 - self.sv["img_h"] / 2))
        win.blit(self.sv["tm_images"][0][0],
                 (setup.win_w / 2 - self.sv["img_w"] / 2, setup.win_h / 2 - self.sv["img_h"] / 2))

    def draw_cursor(self, win, setup):
        bound = self.sv["tm_images"][self.cursor][2]
        rect = pygame.Rect(setup.win_w / 2 - self.sv["img_w"] / 2 + bound[0],
                           setup.win_h / 2 - self.sv["img_h"] / 2 + bound[1],
                           bound[2], bound[3])
        pygame.draw.rect(win, (200, 230, 10), rect, 3)

    def del_cursor(self, win, setup):
        rect = pygame.Rect(setup.win_w / 2 - self.sv["img_w"] / 2 - 2,
                           setup.win_h / 2 - self.sv["img_h"] / 2 - 2,
                           self.sv["img_w"] + 2, self.sv["img_h"] + 2)
        win.blit(setup.win_copy, (rect.x, rect.y), rect)

    def cursor_up(self):
        if self.cursor > 0:
            self.cursor -= 1

    def cursor_down(self):
        if self.cursor < len(self.sv["tm_images"]) - 1:
            self.cursor += 1

    def cursor_left(self):
        val = self.sv["tm_images"][self.cursor][1]
        if self.sv["tm_images"][self.cursor][1] > 0:
            val -= 1
        self.sv["tm_images"][self.cursor][1] = val

    def cursor_right(self):
        val = self.sv["tm_images"][self.cursor][1]
        if val < 100:
            val += 1
        self.sv["tm_images"][self.cursor][1] = val

    def draw_spectre(self, win, setup):
        height = 30
        length = 200
        offset = 100
        rect = pygame.Rect(setup.win_w / 2 - length / 2, setup.win_h / 2 - self.sv["img_h"] / 2 - offset, 100,
                           height)
        #        pygame.draw.rect(win, (20, 20, 20), rect)
        for length in range(0, length):
            v = length / 2
            pygame.draw.rect(win, tuple(get_color(v)), (rect.x + length, rect.y, 1, 30))
        line_x = int(setup.win_w / 2 - length / 2 + self.sv["tm_images"][self.cursor][1] * length / 100)

        pygame.draw.line(win, (255, 255, 255), (line_x, rect.y), (line_x, rect.y + height - 1))


def get_boundary(img):
    w, h = img.get_size()
    start_x = w
    start_y = h
    end_x = 0
    end_y = 0

    for x in range(w):
        for y in range(h):
            a = img.get_at((x, y))[3]
            if a > 0:
                if x < start_x:
                    start_x = x
                if y < start_y:
                    start_y = y
                if x > end_x:
                    end_x = x
                if y > end_y:
                    end_y = y
    # boundary = pygame.Rect(start_x, start_y, end_x-start_x, end_y-start_y)
    return [start_x, start_y, end_x - start_x, end_y - start_y]


def fill(img, color):
    w, h = img.get_size()
    new_img = img.copy()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = img.get_at((x, y))[3]
            grey_val = img.get_at((x, y))[0:3]
            grey_val = [v / 255 for v in grey_val]
            new_r = int(r * grey_val[0])
            new_g = int(g * grey_val[1])
            new_b = int(b * grey_val[2])
            new_img.set_at((x, y), pygame.Color(new_r, new_g, new_b, a))
    return new_img


def get_color(val):
    f = 0.23
    r = int(-(val ** 2) * f + 255)
    if r > 255:
        r = 255
    elif r < 0:
        r = 0
    g = int(-((val - 33.33) ** 2) * f + 255)
    if g > 255:
        g = 255
    elif g < 0:
        g = 0
    b = int(-((val - 66.66) ** 2) * f + 255)
    if b > 255:
        b = 255
    elif b < 0:
        b = 0
    r2 = int(-((val - 100) ** 2) * f + 255)
    if r2 > 255:
        r2 = 255
    elif r2 < 0:
        r2 = 0
    r = r + r2
    return r, g, b
