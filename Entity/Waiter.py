import pygame
import random
from math import sqrt
import Entity.Chars as Chars
import Util.Pathfinding as Pathfinding
from Util.Obstacles import Door, Radio

walkDict = {0: 0, 1: 1, 2: 2,
            3: 3, 4: 2, 5: 1,
            6: 0, 7: 4, 8: 5,
            9: 6, 10: 5, 11: 4}

max_guest = 6


class Waiter(Chars.Chrctrs):
    def __init__(self, x, y, width, height, obstacles, inside, Tilemap):
        Chars.Chrctrs.__init__(self, x, y, width, height, 64 / 4, inside, Tilemap)
        # from pack_Kneipenspiel import cell_size
        self.art = 'waiter'
        self.x_old = x
        self.y_old = y
        self.dir = 1
        self.dispcol = (255, 0, 0)
        self.portrait = Chars.Portraits[1]
        self.textcolor = (0, 225, 0)
        self.text_for = Chars.font.render(self.text, 1, self.textcolor)

        self.serv_guest = None
        self.orders_open = {}
        self.waitCount = 50
        self.act = 0  # 0=stehen, 1=laufen, 2=sprechen
        self.busy = False
        self.steps = []
        self.goal = ()
        self.guyCollide = False
        self.walkable = False
        self.talking = False
        self.angryness = 20
        self.tablett_carry = False
        self.tablett = ''
        self.chair = False
        self.talker = self

        for i in obstacles:
            if i.art == 'Theke':
                self.serv_pos = i.serv_pos
        '''
        w, h = self.Tilemap.get_size()                                             # Extent des Images
        for x in range(w):                                                  # Für jeden Pixel in x- ...
            for y in range(h):                                              # ... und in y-Richtung
                a = self.Tilemap.get_at((x, y))                                    # Nehme den Wert (RGBA) ...
                c1, c2, c3, c4 = a[1], a[2], a[0], a[3]
                a = pygame.Color(c1, c2, c3, c4)                  # ... und VERÄNDERE IHN HIER!!!

                self.Tilemap.set_at((x, y), a)                                      # Weise ihn dem Image wieder zu
         '''

    def calc_movement(self, chars, g, coord, win_sizex, win_sizey, wall_sizex, wall_sizey, door_pos, cell_size, clock,
                      obstacles, interactables):
        if self.inside:
            self.x_old = self.x
            self.y_old = self.y
            #        self.angryness -=2

            # self.act = 0         # stehenbleiben
            # self.act = 1         # Pfadfinden
            # self.act = 2         # Laufen

            # Ober bleibt stehen
            if self.act == 0:

                self.walkCount = 0
                self.blitCount = 0

                if self.x == coord[door_pos[0][0]] and self.y == coord[door_pos[0][1]]:
                    for i in interactables:
                        if i.art == 'door':
                            if i.serv_pos == (door_pos[0][0], door_pos[0][1]):
                                if not i.opened:
                                    i.active = True
                                    i.activated = True
                                else:
                                    self.waitCount = 400
                                    self.inside = False
                elif self.x == coord[door_pos[2][0]] and self.y == coord[door_pos[2][1]]:
                    for i in interactables:
                        if i.art == 'stairs':
                            self.waitCount = 400
                            self.inside = False

                # das muss noch umgebaut werden, weil sonst immer wartet der waiter
                else:  # ...oder prüfen ob ein gast im self.serve_guest ist...
                    if self.serv_guest:
                        # wenn man auf dem Bedienfeld steht
                        if self.x == coord[self.serv_guest.serv_pos[0]] and \
                                self.y == coord[self.serv_guest.serv_pos[1]]:
                            if self.orders_open[self.serv_guest][0] == 0:
                                self.orders_open[self.serv_guest][0] = 1

                            elif self.orders_open[self.serv_guest][0] == 1:
                                self.text = random.choice(('Wasselle?', 'Hi, was bekommst du?',
                                                           'Was kann ich dir bringen?', 'Ja, bitte?', 'Wat willste?'))
                                self.text_count = 0
                                self.orders_open[self.serv_guest][0] = 2

                            elif self.orders_open[self.serv_guest][0] == 4:
                                self.text = 'Okidoki!'
                                self.text_count = 0
                                self.orders_open[self.serv_guest][0] = 5

                            elif self.orders_open[self.serv_guest][0] == 5:
                                if self.text_count == 51:
                                    self.orders_open[self.serv_guest][0] = 6
                                    self.act = 1

                            elif self.orders_open[self.serv_guest][0] == 9:
                                if self.text_count == 51:
                                    self.text_count = 0
                                    self.text = random.choice(("Hier, bitteschön!", "Zum Wohl!", "Gerne ;)", "Jo",
                                                               "Ein blindes Huhn trinkt ja auch mal 'n Korn..."))
                                    self.orders_open[self.serv_guest][0] = 10

                            elif self.orders_open[self.serv_guest][0] == 10:
                                if self.text_count == 51:
                                    self.serv_guest.drink = self.orders_open[self.serv_guest][1]
                                    self.serv_guest.sips = 5
                                    self.orders_open[self.serv_guest][0] = 11

                            elif self.orders_open[self.serv_guest][0] == 12:
                                self.orders_open.pop(self.serv_guest)
                                self.act = 1

                        # Wenn man am Thekenplatz steht
                        elif self.x == coord[self.serv_pos[0]] and self.y == coord[self.serv_pos[1]]:
                            if self.orders_open[self.serv_guest][0] == 6:
                                if self.text_count == 51:
                                    self.text = "Ich mixe, mixe, mixe"
                                    self.text_count = 0
                                    self.orders_open[self.serv_guest][0] = 7

                            elif self.orders_open[self.serv_guest][0] == 7:
                                if self.text_count == 51:
                                    # grafiken einbinden!
                                    self.orders_open[self.serv_guest][2] = 1
                                    self.orders_open[self.serv_guest][0] = 8
                                    self.act = 1

                            elif self.orders_open[self.serv_guest][0] == 8:
                                self.text = "So Kinder, der Bölkstoff ist im Anmarsch!"
                                self.text_count = 0
                                # alle gäste mit orders_open == 7 werden jetzt auf 8 gestellt
                                if sum(i[2] for i in
                                       self.orders_open.values()) == sum(i[0] == 8 for i in self.orders_open.values()):
                                    for i in self.orders_open.keys():
                                        if self.orders_open[i][0] == 8:
                                            self.orders_open[i][0] = 9
                                self.tablett_carry = True
                                self.act = 1
                    else:  # ...oder pfadfinden
                        self.act = 1
                        self.waitCount = 50

            # Ober sucht
            elif self.act == 1:
                # Wenn Gäste auf Kellner warten um zu bestellen, suche neues Ziel
                if self.waitCount > 0:  # entweder Warten...
                    self.waitCount -= 1
                else:
                    if self.orders_open != {}:
                        # Er soll sich neuen Gast suchen, wenn:
                        if sum(i[0] == 9 for i in self.orders_open.values()) > 0:
                            # er Geränke rausbringen soll, es also mindestens einen gibt,
                            g_list = []
                            for i in self.orders_open.keys():
                                if self.orders_open[i][0] == 9:
                                    g_list.append(i)
                            # der, welcher abs(tischnr der akt_servpos - tisch-nr)
                            # der gäste in der liste am kliensten ist
                            g_listxy = [[round(sqrt((i.serv_pos[0] - self.x) ** 2 + (i.serv_pos[1] - self.y) ** 2))
                                         for i in g_list]]
                            self.serv_guest = g_list[g_listxy[0].index(min(g_listxy[0]))]
                            goal = self.serv_guest.serv_pos
                            Pathfinding.pathfinding(self, coord, win_sizex, win_sizey, wall_sizex, wall_sizey,
                                                    obstacles, interactables, goal, cell_size)

                        # Summe ( aller gäste, die schon bestellt ) haben < 3 ODER
                        # Wenn Summe ( aller Getränke, die > 0 sind ) == 0 ist:!??!?!?!
                        elif sum(i[0] > 0 for i in self.orders_open.values()) < max_guest and \
                                sum(i[0] > 0 for i in self.orders_open.values()) != len(self.orders_open.keys()):
                            g_list = []
                            for i in self.orders_open.keys():
                                if self.orders_open[i][0] == 0:
                                    g_list.append(i)
                            g_listxy = [[round(sqrt((i.x - self.x) ** 2 + (i.y - self.y) ** 2)) for i in g_list]]
                            self.serv_guest = g_list[g_listxy[0].index(min(g_listxy[0]))]
                            self.orders_open[self.serv_guest][0] = 0
                            goal = self.serv_guest.serv_pos
                            Pathfinding.pathfinding(self, coord, win_sizex, win_sizey, wall_sizex, wall_sizey,
                                                    obstacles, interactables, goal, cell_size)

                        # soll nur zur theke gehen, wenn: maximum der bestellungen erreicht ist  oder
                        elif sum(i[0] in (6, 7, 8) for i in self.orders_open.values()) >= max_guest or \
                                sum(i[0] == (6, 7, 8) for i in
                                    self.orders_open.values()) == sum(i[2] != 0 for i in self.orders_open.values()):
                            g_list = []
                            for i in self.orders_open.keys():
                                if self.orders_open[i][0] == 6:
                                    g_list.append(i)
                            if not g_list:
                                for i in self.orders_open.keys():
                                    if self.orders_open[i][0] == 8:
                                        g_list.append(i)
                            self.serv_guest = g_list[0]
                            goal = self.serv_pos
                            Pathfinding.pathfinding(self, coord, win_sizex, win_sizey, wall_sizex, wall_sizey,
                                                    obstacles, interactables, goal, cell_size)
                    else:
                        self.serv_guest = None

                    # Ziel: Wenn nix zu tun ist soll er an der Theke rumgammeln
                    if self.orders_open == {}:
                        pos_goals = [(2, 2), (2, 3), (2, 4), (2, 5), (16, 5)]
                        for inter in interactables:
                            if isinstance(inter, Door):
                                pos_goals.append(inter.serv_pos)
                        if self.x in coord and self.y in coord:
                            if (coord.index(self.x), coord.index(self.y)) in pos_goals:
                                pos_goals.remove((coord.index(self.x), coord.index(self.y)))
                        goal = random.choice(pos_goals)
                        Pathfinding.pathfinding(self, coord, win_sizex, win_sizey, wall_sizex, wall_sizey,
                                                obstacles, interactables, goal, cell_size)
                    self.act = 2
            if self.act == 2:
                self.blitCount = 0
                if self.waitCount > 0:
                    self.waitCount -= 1
                else:
                    # walkCount wird zurückgesetzt
                    self.walkCount += 1
                    if self.walkCount >= 96:
                        self.walkCount = 0
                    # läuft zum Ziel
                    # wenn Schritte übrig waren, soll er sie laufen, dir (=Direction) wird bestimmt
                    if self.steps:
                        xy = self.steps.pop()
                        self.x = self.x - self.vel * xy[0]
                        self.y = self.y - self.vel * xy[1]
                        if self.x < self.x - self.vel * xy[0]:
                            self.dir = 1

                        elif self.x > self.x - self.vel * xy[0]:
                            self.dir = 3
                        elif self.y < self.y - self.vel * xy[1]:
                            self.dir = 2
                        elif self.y > self.y - self.vel * xy[1]:
                            self.dir = 0
                        self.blitCount = walkDict[self.walkCount // 8]

                        # Kollisionsabfrage
                        if "guy" in chars:
                            self.guyCollide = False
                            if self.dir == 0:
                                if self.x + self.width > chars["guy"].x and self.x < chars["guy"].x + chars["guy"].width and \
                                        self.y < chars["guy"].y + chars["guy"].height and self.y + self.height > chars["guy"].y:
                                    self.guyCollide = True
                            elif self.dir == 1:
                                if self.y + self.height > chars["guy"].y and self.y < chars["guy"].y + chars["guy"].height and \
                                        self.x < chars["guy"].x + chars["guy"].width and self.x + self.width > chars["guy"].x:
                                    self.guyCollide = True
                            elif self.dir == 2:
                                if self.x + self.width > chars["guy"].x and self.x < chars["guy"].x + chars["guy"].width and \
                                        self.y < chars["guy"].y + chars["guy"].height and self.y + self.height > chars["guy"].y:
                                    self.guyCollide = True
                            elif self.dir == 3:
                                if self.y + self.height > chars["guy"].y and self.y < chars["guy"].y + chars["guy"].height and \
                                        self.x < chars["guy"].x + chars["guy"].width and self.x + self.width > chars["guy"].x:
                                    self.guyCollide = True

                            # Kollision
                            # if self.waitCount == 0: #### Achtung: kommt auch darauf an, was player macht!!!!!
                            if self.guyCollide:
                                # Kollide initiiert, wenn aktulle Position != alte Position
                                #                if (self.x, self.y) != (self.x_old, self.y_old):
                                #                   if self.waitCount == 0:

                                # https://stackoverflow.com/questions/32590131/pygame-blitting-text-with-an-escape-character-or-newline
                                self.text = random.choice(('Hau ab du Bob!', 'Ich hau dir den Drömel aus den Quallen!',
                                                           'Zieh die Kackstelzen ein!',
                                                           " ".join(['Hat dir eigentlich schonmal jemand mit nem',
                                                                     'Vorschlaghammer nen Scheitel gezogen?']),
                                                           'Dein Oberstübchen ist wohl schlecht möbliert!',
                                                           " ".join(['Dir spitz ich den Spargel an, bis man dich fürn',
                                                                     'Pfirsich hält.']),
                                                           'Schwing deine Knochen aus meinem Leben!'))
                                self.text_count = 0
                                self.walkCount = 0
                                self.steps.append(xy)
                                self.x = self.x_old
                                self.y = self.y_old
                                self.angryness += 22
                                self.waitCount = random.randint(50, 75)
                                self.act = 2
                                self.blitCount = 0
                    else:
                        self.act = 0
                        # self.waitCount = random.randint(15,50)
                        # Erhöhung pro tick
            if not clock.lastCall and clock.h_m[0] >= 8:
                clock.lastCall = True
                self.text_count = 0
                self.talker = self
                self.text = 'Letzte Runde!!!'

            if clock.h_m[0] >= 10:
                self.angryness += 0.5
                self.text_count = 0
                self.talker = self
                self.text = 'Feierabend, Raus mit euch!!!'

            # Wenn verärgert -> rausschmiss! == Ende
            if self.angryness >= 100:
                chars["guy"].dead = True
                self.blitCount = 0
            self.facing = self.dir

            dirtyrect = pygame.Rect(self.x, self.y, self.width, self.height)
            return dirtyrect
        else:
            for i in interactables:
                if i.art == "door":
                    if i.serv_pos == (door_pos[0][0], door_pos[0][1]):
                        if i.opened:
                            i.active = True
                            i.activated = True
                            self.x = -100
                            self.y = -100
                elif i.art == "stairs":
                    self.x = -100
                    self.y = -100

            if self.waitCount > 0:
                self.waitCount -= 1
            else:
                self.inside = True
                self.x = self.x_old
                self.y = self.y_old
                self.act = 1
