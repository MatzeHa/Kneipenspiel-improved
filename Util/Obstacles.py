import pygame
from Scripts.Util.LoadImages import ObstacleImages

pygame.init()

images = ObstacleImages()


class Obstacle:
    def __init__(self, _id: object, art: object, pic: object, x: object, y: object, width: object, height: object, nr: object = 0, serv_pos: object = (-1, -1)) -> object:
        self.id = _id
        self.art = art
        self.pic = pic
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkable = False
        self.nr = nr
        self.serv_pos = serv_pos
        self.text = ''


class Chalkboard:
    def __init__(self, _id, x, y, width, height, rot):
        self.id = _id
        self.art = "chalkboard"
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rot = rot
        self.walkable = False
        self.active = False

    def draw(self, win):
        win.blit(pygame.transform.rotate(images.img_chalkboard, self.rot), (self.x, self.y))


class Kerze:
    def __init__(self, _id, x, y, width, height, filter_halo, farbe):
        self.id = _id
        self.art = "kerze"
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.walkable = False
        self.active = False
        self.farbe = farbe
        self.counter = 0
        self.rot = False
        self.repaint_pos = (x + round(height/2) - 64, y + round(height / 2) - 64)
        pygame.draw.circle(filter_halo, (255, 255, 0), (round(x+(width/2)), round(y+(height/2))), 64, 0)

    def draw(self, win):
        win.blit(images.img_kerze[self.farbe], (self.x, self.y))

    def repaint(self, win, win_copy2):
        win.blit(win_copy2, self.repaint_pos, (self.repaint_pos[0], self.repaint_pos[1], 128, 128))
        return pygame.Rect(self.repaint_pos[0], self.repaint_pos[1], 128, 128)


class KerzeWand:
    def __init__(self, _id, x, y, width, height, rot, filter_halo):
        self.id = _id
        self.art = "kerze"
        self.active = False
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rot = rot
        self.walkable = False
        self.on = True
        self.repaint_pos = (x + round(height/2) - 64, y + round(height / 2) - 64)

        pygame.draw.circle(filter_halo, (255, 255, 0), (round(x+(width/2)), round(y+(height/2))), 64, 0)

    def draw(self, win):
        win.blit(pygame.transform.rotate(images.img_kerze_wand, self.rot), (self.x, self.y))

    def repaint(self, win, win_copy2):
        win.blit(win_copy2, self.repaint_pos, (self.repaint_pos[0], self.repaint_pos[1], 128, 128))
        return pygame.Rect(self.repaint_pos[0], self.repaint_pos[1], 128, 128)


class Radio:
    def __init__(self, _id, x, y, width, height):
        self.id = _id
        self.art = "radio"
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.walkable = False
        self.active = False
        self.musicCount = 0
        if self.active:
            pygame.mixer.music.play(-1)

    def del_blit(self, win, win_copy):
        dirtyrect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        return dirtyrect

    def calc(self):
        if not self.active:
            self.musicCount = 0
        else:
            self.musicCount += 1
            if self.musicCount >= 90:
                self.musicCount = 0
        dirtyrect = pygame.Rect(self.x, self.y, self.width, self.height)
        return dirtyrect

    def draw_int(self, win, win_copy):
        win.blit(win_copy, (self.x, self.y), (self.x, self.y, self.width, self.height))
        print("musiccount" + str(self.musicCount//10))
        win.blit(images.img_radio[self.musicCount//10], (self.x, self.y))


class Barstool:
    def __init__(self, _id, x, y, width, height, rot, nr, serv_pos):
        self.id = _id
        self.art = "chair"
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.walkable = False
        self.rot = rot
        self.sit = False
        self.nr = nr
        self.serv_pos = serv_pos
        self.active = False

    def draw(self, win):
        win.blit(pygame.transform.rotate(images.img_barstool, self.rot), (self.x, self.y))


class Chair:
    def __init__(self, _id, x, y, width, height, rot, nr, serv_pos):
        self.id = _id
        self.art = "chair"
        self.active = False
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.walkable = False
        self.rot = rot
        self.sit = False
        self.nr = nr
        self.serv_pos = serv_pos

    def draw(self, win):
        win.blit(pygame.transform.rotate(images.img_chair, self.rot), (self.x, self.y))


class Door:
    def __init__(self, _id, x, y, width, height, rot, coord, cell_size, goto):
        self.id = _id
        self.goto = goto
        self.art = "door"
        self.active = False
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.walkable = True
        self.rot = rot
        self.openCount = 0
        self.openClose = False
        self.opened = False

        if self.rot == 0:
            self.serv_pos = (coord["w"].index(self.x + (2*cell_size)), coord["h"].index(self.y - (1*cell_size)))
        elif self.rot == 90:
            self.serv_pos = (coord["w"].index(self.x - (1*cell_size)), coord["h"].index(self.y + (3*cell_size)))
        elif self.rot == 180:
            self.serv_pos = (coord["w"].index(self.x + (4*cell_size)), coord["h"].index(self.y + (1*cell_size)))
            self.y = y - height
        elif self.rot == 270:
            self.serv_pos = (coord["w"].index(self.x + (1*cell_size)), coord["h"].index(self.y - (3*cell_size)))
            self.x = x - width
        if images.rotDict[self.rot] == 1 or images.rotDict[self.rot] == 3:
            old_height = self.height
            self.height = self.width
            self.width = old_height

    def calc(self):
        if self.openClose:
            if not self.opened:
                if self.openCount < 40:
                    self.openCount += 1
                else:
                    self.opened = True
                    self.openClose = False
            elif self.opened:
                if self.openCount > 0:
                    self.openCount -= 1
                else:
                    self.opened = False
                    self.openClose = False
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_int(self, win, win_copy):
        win.blit(win_copy, (self.x, self.y), (self.x, self.y, self.width, self.height))
        win.blit(pygame.transform.rotate(images.img_door[self.openCount//10], self.rot), (self.x, self.y))


class Stairs:
    def __init__(self, _id, x, y, width, height, rot, coord, cell_size):
        self.id = _id
        self.art = "stairs"
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rot = rot
        self.walkable = False
        self.active = False
        # achtung, hier die rotation mit einberechnen!!!
        if self.rot == 0:
            self.serv_pos = (coord.index(self.x + (-1*cell_size)), coord.index(self.y + (2*cell_size)))
        elif self.rot == 90:
            self.serv_pos = (coord.index(self.x + (2*cell_size)), coord.index(self.y + (3*cell_size)))
        elif self.rot == 180:
            self.serv_pos = (coord.index(self.x + (3*cell_size)), coord.index(self.y - (0*cell_size)))
        elif self.rot == 270:
            self.serv_pos = (coord.index(self.x + (0*cell_size)), coord.index(self.y - (1*cell_size)))

    def draw(self, win):
        win.blit(pygame.transform.rotate(images.img_stairs, self.rot), (self.x, self.y))
        pygame.draw.rect(win, (225, 225, 0), (self.serv_pos[0] * 64 + 150, self.serv_pos[1]*64 + 150, 64, 64), 5)