import pygame
import random
import Scripts.Entity.Chars as Chars

pygame.init()

# TODO: load sounds externally
pygame.mixer.pre_init(frequency=25000, size=-16, channels=2)    # , buffer=4096)
pygame.mixer.init()

toc = pygame.mixer.Sound('../Sound/stepHI.wav')
tic = pygame.mixer.Sound('../Sound/stepLO.wav')

walkDict = {0: 0, 1: 1, 2: 2, 3: 3,
            4: 2, 5: 1, 6: 0, 7: 4,
            8: 5, 9: 6, 10: 5, 11: 4}
rotDict = {0: 0, 90: 3, 180: 2, 270: 1}


class Player(Chars.Chrctrs):
    def __init__(self, x, y, width, height, inside, tilemap, vel=16):
        Chars.Chrctrs.__init__(self, x, y, width, height, vel, inside, tilemap)
        # Variablen aus Überklasse Chars
        self.art = 'player'
        self.x_old = x
        self.y_old = y
        self.dispcol = (0, 0, 255)
        self.talk_action = 0
        self.blitCount = 0
        self.collide = False
        self.textcolor = (225, 225, 0)
        self.text_for = Chars.font.render(self.text, 1, self.textcolor)
        self.portrait = Chars.Portraits[0]
        self.walking = False

        self.orderActive = False
        self.orderAction = 0
        self.sit = False
        self.table = 0
        self.serv_pos = (-1, -1)
        self.money = 20
        self.dead = False
        self.drink = False
        self.sips = 0
        self.sipCount = 8
        self.start_game = False
        self.end_game = False
        self.game = ""
        self.travel = False
        self.room = "lvl_main"

    def calc_movement(self, win, chars, g):

        self.x_old = self.x
        self.y_old = self.y

        # walkCount wird für die Animation benutzt
        self.walkCount += 1

        # Pro tick: weniger betrunken und walkCount wird zurückgesetzt
        if self.walkCount >= 96:
            self.walkCount = 0
        if self.drunkenness >= 0.02:
            self.drunkenness -= 0.02

        # Setzen des blitCounts & walkCounts
        # wenn man sitzt
        if self.sit:
            self.draw_sit(chars["waiter"][0], g.drinks)
            self.blitCount = 7
        # wenn man läuft
        elif self.walking:
            self.blitCount = walkDict[self.walkCount // 8]
        # wenn man steht
        else:
            self.blitCount = 0
            self.walkCount = 0
        # Darstellung guy stehend, sitzend, laufend
        # Neue Sounds einspielen und an richtige Stelle setzen!
        if self.walkCount == 4 or self.walkCount == 36 or self.walkCount == 60:
            tic.play()
        elif self.walkCount == 20 or self.walkCount == 52 or self.walkCount == 84:
            toc.play()
        self.draw_drink(win)
        #        self.walking = False   # aufeäumen, steht glaub ich ziemlich oft im text...
        dirtyrect = pygame.Rect(self.x, self.y, self.width, self.height)
        return dirtyrect

    def sit_down(self, active_chair):
        self.x_old = self.x
        self.y_old = self.y
        self.sit = active_chair
        self.x = active_chair.x
        self.y = active_chair.y
        self.walking = False
        self.table = active_chair.nr
        self.serv_pos = active_chair.serv_pos

    def walk(self, chars, obstacles, interactables, setup):
        # wenn betrunken, laufe in random richtung
        r = random.random()
        if r < (self.drunkenness / 100) ** 2:
            self.dir = random.randint(0, 4)
        self.sit = False
        self.walking = True
        # Kollisionsabfrage
        self.collide = False
        if self.dir == 0:
            if self.y - self.vel < setup.wall_h:
                self.collide = True
                self.walking = False
            elif [True for i in chars if self.x + self.width > i.x and self.x < i.x + i.width and
                    self.y - self.vel < i.y + i.height and self.y + self.height - self.vel > i.y]:
                self.collide = True
                self.walking = False
            else:
                for obst in obstacles + interactables:
                    if not obst.walkable:
                        if obst.x + obst.width > self.x > obst.x - self.width and \
                                obst.y + obst.height > self.y - self.vel > obst.y:
                            self.collide = True
                            self.walking = False
                            break
                    elif obst.walkable:     # TODO das kann weg
                        if obst.art == "door":
                            if obst.x + obst.width > self.x > obst.x - self.width and \
                                    obst.y + obst.height > self.y - self.vel > obst.y:
                                        next_screen = True

        elif self.dir == 1:  # rechts
            if self.x + self.width + self.vel > setup.win_w - setup.wall_w:
                self.collide = True
                self.walking = False
            elif [True for i in chars if self.y + self.height > i.y and self.y < i.y + i.height and
                    self.x + self.vel < i.x + i.width and self.x + self.width + self.vel > i.x]:
                self.collide = True
                self.walking = False
            else:
                for obst in obstacles + interactables:
                    if not obst.walkable:
                        if obst.y + obst.height > self.y > obst.y - self.height and \
                                obst.x < self.x + self.width + self.vel < obst.x + obst.width:
                            self.collide = True
                            self.walking = False
                            break
        elif self.dir == 2:  # unten
            if self.y + self.height + self.vel > setup.win_h - setup.wall_h:
                self.collide = True
                self.walking = False

            elif [True for i in chars if self.x + self.width > i.x and self.x < i.x + i.width and
                    self.y + self.vel < i.y + i.height and self.y + self.height + self.vel > i.y]:
                self.collide = True
                self.walking = False
            else:
                for obst in obstacles + interactables:
                    if not obst.walkable:
                        if self.x < obst.x + obst.width and self.x + self.width > obst.x and \
                                obst.y < self.y + self.height + self.vel < obst.y + obst.height:
                            self.collide = True
                            self.walking = False
                            break
        elif self.dir == 3:
            if self.x + self.vel <= setup.wall_w:
                self.collide = True
                self.walking = False
            elif [True for i in chars if self.y + self.height > i.y and self.y < i.y + i.height and
                    self.x - self.vel < i.x + i.width and self.x + self.width - self.vel > i.x]:
                self.collide = True
                self.walking = False
            else:
                for obst in obstacles + interactables:
                    if not obst.walkable:
                        if obst.y + obst.height > self.y > obst.y - self.height and \
                                obst.x + obst.width > self.x - self.vel > obst.x:
                            self.collide = True
                            self.walking = False
                            break
        if not self.collide:
            if self.dir == 0:
                self.y -= self.vel
            if self.dir == 1:
                self.x += self.vel
            if self.dir == 2:
                self.y += self.vel
            if self.dir == 3:
                self.x -= self.vel
