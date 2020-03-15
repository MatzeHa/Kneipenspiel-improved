import pygame

from Util.QuitGame import quit_game
from Util.ScaleImage import scale_image

pygame.init()

pygame.display.set_caption("Matzes Kneipenspiel - Charaktererstellung", "MK")

img_tilemap_guy = pygame.image.load("../graph/chars/guy/guy_BW.png")
#img_tilemap_guy_ok = img_tilemap_guy.copy()
img_guy_BW = {"head": img_tilemap_guy.subsurface((0, 0, 64, 64)),
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

img_head_bw, _ = scale_image(img_guy_BW["head"], 300)
img_head = img_head_bw.copy()
img_shirt_bw, _ = scale_image(img_guy_BW["shirt"], 300)
img_shirt = img_shirt_bw.copy()
img_pants_bw, _ = scale_image(img_guy_BW["pants_sit"], 300)
img_pants = img_pants_bw.copy()
img_shoes_bw, _ = scale_image(img_guy_BW["shoes_sit"], 300)
img_shoes = img_shoes_bw.copy()
img_hands_bw, _ = scale_image(img_guy_BW["hands_sit"], 300)
img_hands = img_hands_bw.copy()
img_w, img_h = img_head.get_size()

bw_list = [img_head_bw, img_shirt_bw, img_pants_bw, img_shoes_bw, img_hands_bw]


class CreateChar:
    def __init__(self, setup):
        self.setup = setup
        self.creation_active = True
        self.timer_clock = pygame.time.Clock()
        self.imgs = {0: [img_head, 0, get_boundary(img_head)],
                     1: [img_shirt, 0, get_boundary(img_shirt)],
                     2: [img_pants, 0, get_boundary(img_pants)],
                     3: [img_shoes, 0, get_boundary(img_shoes)],
                     4: [img_hands, 0, get_boundary(img_hands)]}
        self.cursor = 0
        self.new_tilemap = None

    def start_creation(self, win):
        self.init_blit(win)
        self.run(win)
        self.new_tilemap = self.create_tilemap(win)

    def init_blit(self, win):
        self.draw_spectre(win)
        self.draw_all(win)
        self.setup.win_copy = win.copy()

    def run(self, win):
        run = True
        while run:
            change_color_ok = False
            self.del_cursor(win)
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
            self.draw_spectre(win)
            if change_color_ok:
                self.change_color(self.cursor)
            self.draw_all(win)
            self.draw_cursor(win)

            self.timer_clock.tick(30)
            # print("FPS: ", self.timer_clock.get_fps())
            pygame.display.update()

    def create_tilemap(self, win):
        from random import randint
        tilemap = pygame.Surface([512, 512], pygame.SRCALPHA, 32)
        tilemap = tilemap.convert_alpha()

        if self.creation_active:
            col_head = get_color(self.imgs[0][1])
            col_shirt = get_color(self.imgs[1][1])
            col_shoes = get_color(self.imgs[3][1])
            col_hands = get_color(self.imgs[4][1])
            col_pants = get_color(self.imgs[2][1])
        else:
            col_head = get_color(randint(0, 100))
            col_shirt = get_color(randint(0, 100))
            col_shoes = get_color(randint(0, 100))
            col_hands = get_color(randint(0, 100))
            col_pants = get_color(randint(0, 100))

        head = fill(img_guy_BW["head"], col_head)
        shirt = fill(img_guy_BW["shirt"], col_shirt)

        walk0_shoes = fill(img_guy_BW["shoes_walk0"], col_shoes)

        walk1_hands = fill(img_guy_BW["hands_walk1"], col_hands)
        walk1_shoes = fill(img_guy_BW["shoes_walk1"], col_shoes)

        walk2_hands = fill(img_guy_BW["hands_walk2"], col_hands)
        walk2_shoes = fill(img_guy_BW["shoes_walk2"], col_shoes)
        walk2_pants = fill(img_guy_BW["pants_walk2"], col_pants)

        walk3_hands = fill(img_guy_BW["hands_walk3"], col_hands)
        walk3_shoes = fill(img_guy_BW["shoes_walk3"], col_shoes)
        walk3_pants = fill(img_guy_BW["pants_walk3"], col_pants)

        sit_hands = fill(img_guy_BW["hands_sit"], col_hands)
        sit_shoes = fill(img_guy_BW["shoes_sit"], col_shoes)
        sit_pants = fill(img_guy_BW["pants_sit"], col_pants)

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
        img = bw_list[cursor]
        col = get_color(self.imgs[cursor][1])
        self.imgs[cursor][0] = fill(img, col)
        return self.imgs[cursor][0]

    def draw_all(self, win):
        win.blit(self.imgs[4][0], (self.setup.win_w/2 - img_w/2, self.setup.win_h/2 - img_h/2))
        win.blit(self.imgs[3][0], (self.setup.win_w/2 - img_w/2, self.setup.win_h/2 - img_h/2))
        win.blit(self.imgs[2][0], (self.setup.win_w/2 - img_w/2, self.setup.win_h/2 - img_h/2))
        win.blit(self.imgs[1][0], (self.setup.win_w/2 - img_w/2, self.setup.win_h/2 - img_h/2))
        win.blit(self.imgs[0][0], (self.setup.win_w/2 - img_w/2, self.setup.win_h/2 - img_h/2))

    def draw_cursor(self, win):
        bound = self.imgs[self.cursor][2]
        rect = pygame.Rect(self.setup.win_w/2 - img_w/2 + bound[0],
                           self.setup.win_h/2 - img_h/2 + bound[1],
                           bound[2], bound[3])
        pygame.draw.rect(win, (200, 230, 10), rect, 3)

    def del_cursor(self, win):
        rect = pygame.Rect(self.setup.win_w/2 - img_w/2 - 2,
                           self.setup.win_h/2 - img_h/2 - 2,
                           img_w + 2, img_h + 2)
        win.blit(self.setup.win_copy, (rect.x, rect.y), rect)

    def cursor_up(self):
        if self.cursor > 0:
            self.cursor -= 1

    def cursor_down(self):
        if self.cursor < len(self.imgs)-1:
            self.cursor += 1

    def cursor_left(self):
        val = self.imgs[self.cursor][1]
        if self.imgs[self.cursor][1] > 0:
            val -= 1
        self.imgs[self.cursor][1] = val

    def cursor_right(self):
        val = self.imgs[self.cursor][1]
        if val < 100:
            val += 1
        self.imgs[self.cursor][1] = val

    def draw_spectre(self, win):
        height = 30
        length = 200
        offset = 100
        rect = pygame.Rect(self.setup.win_w / 2 - length/2, self.setup.win_h/2 - img_h/2 - offset, 100, height)
#        pygame.draw.rect(win, (20, 20, 20), rect)
        for length in range(0, length):
            v = length/2
            pygame.draw.rect(win, tuple(get_color(v)), (rect.x + length, rect.y, 1, 30))
        line_x = int(self.setup.win_w/2 - length/2 + self.imgs[self.cursor][1] * length/100)

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
    return [start_x, start_y, end_x-start_x, end_y-start_y]


def fill(img, color):
    w, h = img.get_size()
    new_img = img.copy()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = img.get_at((x, y))[3]
            grey_val = img.get_at((x, y))[0:3]
            grey_val = [v/255 for v in grey_val]
            new_r = int(r*grey_val[0])
            new_g = int(g*grey_val[1])
            new_b = int(b*grey_val[2])
            new_img.set_at((x, y), pygame.Color(new_r, new_g, new_b, a))
    return new_img


def get_color(val):
    f = 0.23
    r = int(-(val**2) * f + 255)
    if r > 255:
        r = 255
    elif r < 0:
        r = 0
    g = int(-((val-33.33)**2) * f + 255)
    if g > 255:
        g = 255
    elif g < 0:
        g = 0
    b = int(-((val-66.66)**2) * f + 255)
    if b > 255:
        b = 255
    elif b < 0:
        b = 0
    r2 = int(-((val-100)**2) * f + 255)
    if r2 > 255:
        r2 = 255
    elif r2 < 0:
        r2 = 0
    r = r + r2
    return r, g, b
