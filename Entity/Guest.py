import pygame
import random
import Util.Pathfinding as Pathfinding
import Entity.Chars as Chars
import Util.DialogScript as DialogSkript
# Guest_sit = pygame.image.load('graph/chars/guy/Guy_sit.png')
rotDict = {0: 0, 90: 3, 180: 2, 270: 1}

pygame.init()


walkDict = {0: 0, 1: 1, 2: 2,
            3: 3, 4: 2, 5: 1,
            6: 0, 7: 4, 8: 5,
            9: 6, 10: 5, 11: 4}
# rotDict = {0: 0, 90: 3, 180: 2, 270: 1}
# text_count_max = 51


order_timer = 200


class Guest(Chars.Chrctrs):
    def __init__(self, x, y, width, height, vel, chair, walk_in, inside):
        Chars.Chrctrs.__init__(self, -100, 100, width, height, vel, inside)
        self.art = 'guest'                                                         # zurzeit: spieler, guest, waiter...
        self.x_old = x                                                             # alte Position x
        self.y_old = y                                                             # alte Position y
        self.dispcol = (0, 0, 255)
        self.portrait = Chars.Portraits[random.randint(1, 6)]
        self.textcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # zufällige Farbe
        self.text_for = Chars.font.render(self.text, 1, self.textcolor)            # Formatieren des Textes zum blitten

        self.version = random.randint(0, len(DialogSkript.Dialoge.keys())-1)
        self.going = False
        self.coming = True
        self.bladderTime = -1
        self.chair = chair                                                      # Objekt Chair, auf dem Gast sitzen soll
        self.goal = (chair.x, chair.y)                                             # Zugewiesenes Ziel
        self.sit = False                                                           # sitzt noch nicht
        self.drink = False                                              # Drink in der Hand
        self.sips = 0
        self.sipCount = 8                                                          # Schlücke übrig
        self.serv_pos = ()
        self.collide = False
        self.walk_in = walk_in                                                     # Uhrzeit des Eintritts
        self.steps = []                                                            # Keine steps mehr im Speicher
        self.guyCollide = False                                                    # Wenn Kellner kollidiert
        self.actionCount = 0                                                       # Action Zähler
        self.order_timer = random.randint(50, 70)
        self.orderActive = False
        self.orderAction = 0
        self.orderAct = 0
        # self.angryness = 0
        self.siptime = 50
        self.waitCount = 0
        self.toilet = False
        self.lastAction = None
        self.mustblit = True
        self.talk_further = True

#

    def calc_movement(self, g, coord, win_sizex, win_sizey, wall_sizex, wall_sizey, cell_size):
        if self.inside:
            self.mustblit = True

            self.x_old = self.x                     # x von letztem frame wird gepeichert>
            self.y_old = self.y                     # Y von letztem frame wird gepeichert>

            # Pro tick: walkCount wird zurückgesetzt ### und weniger betrunken
            self.walkCount += 1                     # walkCount wird für die Animation benutzt
            if self.walkCount >= 96:
                self.walkCount = 0

            # Take a Sip
            if self.sips > 0:
                print(self.drink)
                if self.siptime > 0:
                    self.siptime -= 1
                if self.siptime == 0:
                    self.sipCount = 0
                    self.siptime = random.randint(100, 400)
                    self.sips -= 1
                    self.drunkenness = self.drunkenness + drinks[self.drink][2]
                    if self.drunkenness > 100:
                        self.drunkenness = 100
                    # randomisieren
                    if self.bladderTime < 0:
                        self.bladderTime = random.randint(200, 1000)
                        self.toilet = True

            # setting goals
            # türe
            if not self.going and g.clock.lastCall and self.x in coord and self.y in coord:
                self.goal = (coord[g.door_pos[1][0]], coord[g.door_pos[1][1]])
                self.going = True
                self.sit = False
            # klo
            elif self.bladderTime > 0:
                self.bladderTime -= 1
            elif self.bladderTime == 0 and self.x in coord and self.y in coord and self.toilet:
                self.goal = (coord[g.door_pos[2][0]], coord[g.door_pos[2][1]])
                self.text = random.choice(('Ich muss mal verschwindibussen...', 'Oh, oh, das Bläschen drückt...',
                                           'Ich muss pissen!', 'Ich muss kurz das große Latrinum aufsagen gehen...',
                                           'Ich geh mal die Nougatschleuse öffnen...', 'Puh, Darmdrücken...',
                                           'SCHEISSE!', 'Huch, ich empfange ein Fax aus Darmstadt',
                                           'Ich geh mir kurz n Snickers aus dem Rücken drücken',
                                           'Ich geh kurz nen Bob in die Bahn werfen...',
                                           'Puh, ich muss mal kurz ins Harnstudio gehen...'))
                self.toilet = False
                self.text_count = 0
                self.sit = False

            # pfadfinden
            if self.goal != () and self.steps == []:
                Pathfinding.pathfinding(self, coord, win_sizex, win_sizey, wall_sizex, wall_sizey,
                                        g.obstacles, g.interactables, self.goal, cell_size)
                self.goal = ()
            # Positionsabfrage
            # Gast setzt sich
            if (self.x == self.chair.x and self.y == self.chair.y) and not self.sit and self.steps == []:
                self.sit = self.chair
                self.chair.active = True
                self.dir = rotDict[self.chair.rot]
                self.walking = False
                self.serv_pos = self.chair.serv_pos
            # gast geht aus tür
            elif self.x == coord[g.door_pos[1][0]] and self.y == coord[g.door_pos[1][1]] and self.steps == []:
                self.inside = False
            # gast geht in keller
            elif (self.x == coord[g.door_pos[2][0]] and self.y == coord[g.door_pos[2][1]]) and self.bladderTime >= 0:
                self.waitCount = random.randint(100, 500)
                self.inside = False

            # Gast hat sich gesetzt
            if self.sit:
                # if self.lastAction != 'sit':
                self.draw_sit(g.waiter[0], g.drinks)
                self.blitCount = 7
            # else:
            #    self.mustblit = False

            # wenn Schritte übrig sind, soll er sie laufen, dir (=Direction) wird bestimmt
            elif self.steps:
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

                # Kollisionsabfrage
                if self.collide and self.text_count > 0:
                    self.talk_further = True
                elif self.text_count == 0:
                    self.talk_further = False
                self.collide = False
                if self.dir == 0:
                    if self.x + self.width > g.guy.x and self.x < g.guy.x + g.guy.width and \
                            self.y < g.guy.y + g.guy.height and self.y + self.height > g.guy.y:
                        self.collide = True
                elif self.dir == 1:
                    if self.y + self.height > g.guy.y and self.y < g.guy.y + g.guy.height and \
                            self.x < g.guy.x + g.guy.width and self.x + self.width > g.guy.x:
                        self.collide = True
                elif self.dir == 2:
                    if self.x + self.width > g.guy.x and self.x < g.guy.x + g.guy.width and \
                            self.y < g.guy.y + g.guy.height and self.y + self.height > g.guy.y:
                        self.collide = True
                elif self.dir == 3:
                    if self.y + self.height > g.guy.y and self.y < g.guy.y + g.guy.height and \
                            self.x < g.guy.x + g.guy.width and self.x + self.width > g.guy.x:
                        self.collide = True

                    # Kollision
                if self.collide:
                    if not self.talk_further:
                        self.text_count = 0
                    self.text = "Weg da!"
                    self.walkCount = 0
    #                self.angryness += 33
                    self.actionCount += 1
                    self.steps.append(xy)
                    self.x = self.x + self.vel * xy[0]
                    self.y = self.y + self.vel * xy[1]

                    # Erhöhung pro tick
    #                    self.actionCount -= 1

    #        if self.walking == True:
                self.blitCount = walkDict[self.walkCount // 8]
                self.facing = self.dir
                self.sit = False
                self.walking = True

            # wenn man steht
            else:
                self.blitCount = 0
                self.walkCount = 0

            # Aktualisieren der letzten Aktion
            if self.sit:
                self.lastAction = 'sit'
            elif self.sipCount < 8:
                self.lastAction = 'drink'
            elif self.x != self.x_old and self.y != self.y_old:
                self.lastAction = 'walk'
            elif self.x == self.x_old and self.y == self.y_old:
                self.lastAction = 'stand'

            dirtyrect = pygame.Rect(self.x, self.y, self.width, self.height)
            return dirtyrect

        else:
            self.mustblit = True
            if not self.going:
                for i in g.interactables:
                    if i.art == 'door' and i.serv_pos == (g.door_pos[1][0], g.door_pos[1][1]) and self.coming:
                        if not i.opened:
                            i.active = True
                            i.openClose = True
                        else:
                            self.inside = True
                            self.x = self.x_old
                            self.y = self. y_old
                            i.active = True
                            i.openClose = True
                            self.coming = False

                    elif i.art == 'stairs' and i.serv_pos == (g.door_pos[2][0], g.door_pos[2][1]) and self.bladderTime == 0:
                        print("im Keller")
                        self.x = -100
                        self.y = -100
                        if self.waitCount > 0:
                            self.waitCount -= 1
                        if self.waitCount == 0:
                            self.x = coord[g.door_pos[2][0]]
                            self.y = coord[g.door_pos[2][1]]
                            self.inside = True
                            self.bladderTime = -1
                            self.goal = (self.chair.x, self.chair.y)
            if self.going:
                for i in g.interactables:
                    if i.art == 'door' and i.serv_pos == (g.door_pos[1][0], g.door_pos[1][1]):
                        if not i.opened:
                            i.active = True
                            i.openClose = True
                        else:
                            self.inside = False
                            self.mustblit = False
