import pygame

pygame.init()

class Entity:
    def __init__(self):
        self.pos_x = 64
        self.pos_y = 128
        self.width = 32
        self.height = 32
        self.move_h = 0
        self.move_v = 0
        self.vel = 4
        self.dirtyrect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def movement(self):
        self.dirtyrect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.pos_x += self.move_h
        self.pos_y += self.move_v
        self.dirtyrect = pygame.Rect.union(pygame.Rect(self.pos_x, self.pos_y, self.width, self.height),
                                           self.dirtyrect)
        return self.dirtyrect

    def overblit(self, win, setup):
        if self.move_h < 0 or self.move_h > 0:  # links oder rechts
            win.blit(setup.win, (self.pos_x, self.pos_y),
                     (self.pos_x, self.pos_y, self.move_h, self.height))
        if self.move_v < 0 or self.move_v > 0:  # hoch oder runter
            win.blit(setup.win, (self.pos_x, self.pos_y),
                     (self.pos_x, self.pos_y, self.width, self.move_v))



    def blitten(self, win):
        win.fill((255, 0, 0), (self.pos_x, self.pos_y, self.width, self.height))


    def random_walk(self):
        import random
        d = random.randint(0, 5)
        if d == 0:
            self.move_h = -random.randint(0, 5)
            self.move_v = 0
        elif d == 1 or dir == 4:
            self.move_h = random.randint(0, 5)
            self.move_v = 0
        elif d == 2:
            self.move_h = 0
            self.move_v = -random.randint(0, 5)
        elif d == 3:
            self.move_h = 0
            self.move_v = random.randint(0, 5)