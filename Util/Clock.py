import pygame
import math


class Clock:
    def __init__(self, _id, x, y):
        self.id = _id

        self.x = x
        self.y = y
        self.r = 35
        self.tick = 0
        self.h_m = (6, 0)
        self.lastCall = False
        self.m_x = self.m_y = self.h_x = self.h_y = 0

    def calc(self):
        # WARUM? weil 1Tag = 24 h = 1400 min
        # 1 h = 60 ticks
        # 1 min =1 tick

        self.m_x = self.x - math.cos(3 * self.tick * math.pi / 180) * self.r * 0.8
        self.m_y = self.y - math.sin(3 * self.tick * math.pi / 180) * self.r * 0.8

        self.h_x = self.x + math.cos((15 * self.tick // 60) * math.pi / 180) * self.r * 0.6
        self.h_y = self.y + math.sin((15 * self.tick // 60) * math.pi / 180) * self.r * 0.6

        self.h_m = (math.floor(self.tick / 120), (self.tick / 2) % 60)
        self.tick += .1
        if self.tick == 1440:
            self.tick = 0
        return pygame.Rect(self.x - 32, self.y - 32, 64, 64)

    def draw(self, win):
        pygame.draw.circle(win, (200, 200, 200), (self.x, self.y), self.r - 2, 0)
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.r, 3)
        # minuten
        pygame.draw.line(win, (0, 0, 150), (self.x, self.y), (self.m_x, self.m_y), 2)
        # stunden
        pygame.draw.line(win, (150, 0, 0), (self.x, self.y), (self.h_x, self.h_y), 4)
