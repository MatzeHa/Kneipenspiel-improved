import pygame
import random

# Images
pygame.init()

font = pygame.font.SysFont('Courier', 30, True)
ground = pygame.image.load('../Graph/GUI/floor_big.png')
Tilemap = pygame.image.load('../Graph/chars/guy/tilemap_chars.png')
# Tilemap = pygame.image.load('../Graph/chars/guy/tilemap_chars_no.png')

spcl_chars = ['\'', '-', '~', '*', '*hicks*']
drunk_dict = {"a": "@", "A": "@", "b": "3", "B": "3", "c": "c", "C": "C", "d": "d", "D": "D", "e": "€", "E": "€",
              "f": "f", "F": "F", "g": "G", "G": "g", "h": "h", "H": "H", "i": "ä", "I": "Ä", "j": "y", "J": "Y",
              "k": "g", "K": "G", "l": "l", "L": "L", "m": "m", "M": "m", "n": "ng", "N": "M", "o": "0", "O": "0",
              "p": "bb", "P": "b", "q": "Q", "Q": "q", "r": "r", "R": "R", "s": "S", "S": "S", "t": "t", "T": "T",
              "u": "u", "U": "U", "v": "f", "V": "F", "w": "W", "W": "w", "x": "iks", "X": "IKS", "y": "y", "Y": "Y",
              "z": "c", "Z": "C"}

Portraits = [pygame.image.load('../Graph/chars/guy/port_g0.png'), pygame.image.load('../Graph/chars/guy/port_g1.png'),
             pygame.image.load('../Graph/chars/guy/port_g2.png'), pygame.image.load('../Graph/chars/guy/port_g3.png'),
             pygame.image.load('../Graph/chars/guy/port_g4.png'), pygame.image.load('../Graph/chars/guy/port_g5.png'),
             pygame.image.load('../Graph/chars/guy/port_g6.png')]
name_list = ["Albert Tross", "Alexander Platz", "Ali Baba", "Alter, Fritz", "Andi Mauer", "Andreas Kreuz", "Ann Geber",
             "Ann Zug", "Anna Bolika", "Anna Gramm", "Anna Liese", "Anna Nass", "Anna Theke", "Anne Wand", "Apple Blythe Allison",
             "Aquinnah Kathleen", "Audio Science Clayton", "Axel Flecken", "Axel Haar", "Axel Höhle", "Axel Schweiß",
             "Bernhard Diener", "Bill Ich", "Bill Yard", "Billibald", "Blue Angel", "Bluebell Madonna", "Bob Fahrer", "Bren Essel",
             "Bronx Mowgli", "Chastitiy Sun", "Cheyenne Savannah", "Claire Bazyn", "Claire Grube", "Claire Waßer", "Daisy Boo",
             "Deinhard", "Demut", "Dick Erchen", "Dick S.Ding", "Dick Tator", "Diva Thin Muffin Pigeen", "Donalde Duck",
             "Dr.Acula", "Ed Ding", "Eitelfritz", "Elijah Blue", "Elijah Bob Patricius Guggi", "Ellen Lang", "Elli Fant",
             "Eric fik van Hinten",  "Erlfried König", "Ernst Fall", "Ernst Haft", "Eutropia", "Eva Adam", "Eva N.Gelium",
             "Fanny Knödel", "Fifi Trixibelle", "Florida", "Frank Reich", "Frankobert", "Franz Brandwein", "Franz Mann",
             "Franz Ohse", "Georg Asmus", "Gerd Nehr",  "Gerold Steiner", "Gracie Fan", "Gregor Janisch",
             "Grier Hammond Henchy", "Gutfried Wurst", "Hans A. Bier",  "Hans Dampf", "Hans Maul", "Hans Wurst",
             "Harlow Winter Kate", "Harry Bo", "Hasta La vista", "Heavenly Hiraani Tiger Lily", "Heide Witzka", "Heidi Kraut",
             "Hein Blöd", "Heinz Ellmann", "Heinz Elmann", "Heinz Fiction", "Hella Kot", "Hella Wahnsinn",
             "Henry Günther Ademola Dashtu Samuel", "Herr Bert Herbert", "Herta Wurst", "Herta Zuschlag", "Hugo Slawien",
             "Ireland Eliesse", "Jake Daniel", "James Bond", "Jesus Halleluja", "Jim Panse", "Jimi Blue", "Jo Ghurt", "Jo Ker",
             "Johannes Beer", "Johannes Brodt", "Johannes Burg", "Johannes Kraut", "Johannis Bär", "Johannis Burg", "John Glör",
             "John Jack", "Johnny Walker", "K. Melle", "Kai Mauer", "Kai Sehr", "Kai Ser", "Karel Ofen", "Karl Auer", "Karl Ender",
             "Karl Kopf", "Karl Sruhe", "Karo Kästchen", "Ken Tucky", "Kid Zler", "Klara Bach", "Klara Fall", "Klara Geist",
             "Klara Himmel", "Klara Korn", "Klaus Thaler", "Klaus Trophobie", "Klaus Uhr", "Knut Schfleck", "Lars Samenström",
             "Lee Kör", "Lilly Putaner", "Lisa Bonn", "Manne Quinn", "Marga Käse", "Marga Milch", "Maria Kron", "Maria Zell",
             "Marie Huana", "Marie Juana", "Mario Nese", "Mark Aber", "Mark Graf", "Markus Platz", "Marta Pfahl", "Martha Hari",
             "Mary Huana", "Melitta Mann", "Mira Bellenbaum", "Miss Raten", "Muh Barack", "Nick Olaus", "Olga Machslochoff",
             "Olle Schleuder", "Otto Päde", "Pan Tau", "Paul Ahner", "Paul Lahner", "Peer Verser", "Pepsi-Carola", "Perry Ode",
             "Peter Pan", "Peter Petersilie", "Peter Silie", "Phil Fraß", "Philip Morris", "Polly Zist", "Rainer Hohn",
             "Rainer Müll", "Rainer Stoff", "Rainer Verlust", "Rainer Wein", "Rainer Zufall", "Reiner Korn", "Reiner Zorn",
             "Reiner Zufall", "Rob Otter", "Roman Schreiber", "Roman Ticker", "Roman Tisch", "Ron Dell", "Rosa Fingernagel",
             "Rosa Fleisch", "Rosa Himmel", "Rosa Hirn", "Rosa Panter", "Rosa Rosenbusch", "Rosa Roth", "Rosa Schwein",
             "Rosa Wolke", "Rosa Wurst", "Rosi Ne", "Rudi Mentation", "Sham Paine", "Speck Wildhorse", "Sunny Täter", "Teddy Baer",
             "Thor Schuß", "Tim Buktu", "Tscherno Bill", "Ute Russ", "Wilma Bier", "Wilma Gern", "Wilma Haschen",
             "Wilma Pfannkuchen", "Wilma Ruhe", "Wilma Streit", "Wolfgang See"]

walkDict = {0: 0, 1: 1, 2: 2,
            3: 3, 4: 2, 5: 1,
            6: 0, 7: 4, 8: 5,
            9: 6, 10: 5, 11: 4}
rotDict = {0: 0, 90: 3, 180: 2, 270: 1}
cellSize = 64


class Chrctrs:
    def __init__(self, x, y, width, height, vel, inside, tilemap=None):
        # Variables just for certain Characters
        self.orderAction = None
        self.order_timer = None
        self.drink = None
        self.sit = None
        self.sips = None
        self.sipCount = None
        self.tablett_carry = None
        self.orderActive = None
        self.textcolor = None
        self.text_for = None

        # Variables for all Characters
        self.art = ""
        self.x = x
        self.y = y
        self.x_old = x
        self.y_old = y
        self.width = width
        self.height = height
        self.vel = vel
        self.walkCount = 0
        self.dir = 0
        self.facing = 0
        self.walking = False
        self.text = ''
        self.text_count = 51
        self.dispcol = (0, 0, 0)
        self.inside = inside
        self.drunkenness = random.randint(0, 40)
        self.blitCount = 0
        self.walkCount = 0
        self.name = random.choice(name_list)
        if not tilemap:
            self.Tilemap = Tilemap
        else:
            self.Tilemap = tilemap.convert_alpha()

    def del_blit(self, win, win_copy):
        dirtyrect = pygame.Rect(self.x_old, self.y_old, self.width, self.height)
        win.blit(win_copy, (self.x_old, self.y_old), dirtyrect)
#        if self.text_count < 51:
#            self.del_text()
#        self.del_display(win, win_copy)
        return dirtyrect

    def talk(self, win):
        dirtyrect = pygame.Rect(self.x - 64, self.y - cellSize,
                                self.text_for.get_width(),
                                self.text_for.get_height())
        if self.text_count == 0:

            text_new = self.drunk_text(self.text)

            self.text_for = font.render(text_new, 1, self.textcolor)
        win.blit(self.text_for, (dirtyrect.x, dirtyrect.y))
        return dirtyrect

    def drunk_text(self, text):
        new_text = ""
        for p in text:
            spcl = random.randint(60, 100)
            if spcl < self.drunkenness:
                p = p + random.choice(spcl_chars)
            gurgle = random.randint(0, 100)
            if gurgle < self.drunkenness:
                if p in drunk_dict.keys():
                    new_text = new_text + drunk_dict[p]
                else:
                    new_text = new_text + p
            else:
                new_text = new_text + p
        return new_text

    def del_text(self, win, win_copy):
        dirtyrect = pygame.Rect(self.x_old - 64 - self.vel, self.y_old - cellSize - self.vel,
                                self.text_for.get_width() + self.vel * 2,
                                self.text_for.get_height() + self.vel * 2)
        win.blit(win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        self.text_count += 1
        return dirtyrect

    def calc_display(self):
        # Angryness/-Drunkenness-Balken über der Köpfen anzeigen
        dirtyrect = pygame.Rect(self.x - 20, self.y - 32, 110, 14)
        return dirtyrect

    def draw_display(self, win, unit):
        pygame.draw.rect(win, (150, 150, 150), (self.x - 20, self.y - 32, 110, 14), 0)  # Grauer Hintergrund
        pygame.draw.rect(win, self.dispcol, (self.x - 17, self.y - 29, unit, 8), 0)  # Darstellung der Einheit
        for i in range(0, 10):  # Schwarze Kästchen für Abgryness-Display
            pygame.draw.rect(win, (10, 10, 10), (self.x - 18 + i * 10, self.y - 30, 10, 10), 2)

    def del_display(self, win, win_copy):
        dirtyrect = pygame.Rect(self.x_old - 20 - self.vel, self.y_old - 32 - self.vel,
                                110 + self.vel * 2, 14 + self.vel * 2)
        win.blit(win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        return dirtyrect

    def draw_char(self, win):
        if self.facing == 0:  # rauf
            win.blit(self.Tilemap, (self.x, self.y), (self.blitCount * 64, 0, 64, 64))  # Waiter
        elif self.facing == 1:  # rechts
            win.blit(pygame.transform.rotate(self.Tilemap, 270), (self.x, self.y),
                     (self.Tilemap.get_width() - 64, self.blitCount * 64, 64, 64))
        elif self.facing == 2:  # runter
            win.blit(pygame.transform.flip(self.Tilemap, True, True), (self.x, self.y),
                     (self.Tilemap.get_width() - 64 * (self.blitCount + 1), self.Tilemap.get_height() - 64, 64, 64))
        elif self.facing == 3:  # links
            win.blit(pygame.transform.rotate(self.Tilemap, 90), (self.x, self.y),
                     (0, self.Tilemap.get_height() - (self.blitCount + 1) * 64, 64, 64))
        if self.art == 'waiter':
            if self.tablett_carry:
                self.draw_tablett(win)
        else:
            self.draw_drink(win)

    def draw_tablett(self, win):
        if self.dir == 0:  # rauf
            win.blit(self.Tilemap, (self.x, self.y), (0, 64 * 2, 64, 64))  # Tablett
        elif self.dir == 1:  # rechts
            win.blit(pygame.transform.rotate(self.Tilemap, 270), (self.x, self.y),
                     (self.Tilemap.get_width() - 64 * 3, 0, 64, 64))
        elif self.dir == 2:  # runter
            win.blit(pygame.transform.flip(self.Tilemap, True, True), (self.x, self.y),
                     (self.Tilemap.get_width() - 64, self.Tilemap.get_height() - (64 * 3), 64, 64))
        elif self.dir == 3:  # links
            win.blit(pygame.transform.rotate(self.Tilemap, 90), (self.x, self.y),
                     (64 * 2, self.Tilemap.get_height() - 64, 64, 64))

    def draw_drink(self, win):
        # Getränk in Hand
        if self.drink:
            if self.sipCount == 8:
                if self.facing == 0:
                    win.blit(Tilemap, (self.x, self.y), (self.drink * 64, 64, 64, 64))
                elif self.facing == 1:
                    win.blit(pygame.transform.rotate(Tilemap, 270), (self.x, self.y),
                             (Tilemap.get_width() - 64 * 2, self.drink * 64, 64, 64))
                elif self.facing == 2:
                    win.blit(pygame.transform.flip(Tilemap, True, True), (self.x, self.y),
                             (Tilemap.get_width() - 64 * (self.drink + 1), Tilemap.get_height() - 64 * 2, 64, 64))
                elif self.facing == 3:
                    win.blit(pygame.transform.rotate(Tilemap, 90), (self.x, self.y),
                             (64, Tilemap.get_height() - (self.drink + 1) * 64, 64, 64))

            # Trinkanimation
            if self.sipCount < 8:
                if self.facing == 0:
                    win.blit(Tilemap, (self.x + self.sipCount, self.y + self.sipCount), (self.drink * 64, 64, 64, 64))
                elif self.facing == 1:
                    win.blit(pygame.transform.rotate(Tilemap, 270), (self.x - self.sipCount, self.y + self.sipCount),
                             (Tilemap.get_width() - 64 * 2, self.drink * 64, 64, 64))
                elif self.facing == 2:
                    win.blit(pygame.transform.flip(Tilemap, True, True),
                             (self.x - self.sipCount, self.y - self.sipCount),
                             (Tilemap.get_width() - 64 * (self.drink + 1), Tilemap.get_height() - 64 * 2, 64, 64))
                elif self.facing == 3:
                    win.blit(pygame.transform.rotate(Tilemap, 90), (self.x + self.sipCount, self.y - self.sipCount),
                             (64, Tilemap.get_height() - (self.drink + 1) * 64, 64, 64))
                self.sipCount += 1

            if self.sips == 0 and self.sipCount == 8:
                self.drink = 0
            if self.art == 'guest':
                self.order_timer = random.randint(100, 1000)

    def draw_sit(self, waiter, drinks):
        self.walkCount = 0
        self.facing = rotDict[self.sit.rot]
        if self.art == 'guest' and self.order_timer > 0:
            self.order_timer -= 1
        if self.art == 'guest':
            if self.order_timer == 0:
                self.order_timer = -1
                waiter.orders_open.update({self: [0, 0, 0]})
                self.text = random.choice(('Hey, Ober!', 'Wirtschaaaft!', 'Komma her, Digga!'))
                self.text_count = 0
        elif self.art == 'player' and self.orderActive:
            if self.orderAction == 0:
                if self.text_count == 51:
                    self.text = 'ICH WILL BESTELLEN!!!'
                    self.text_count = 0
                    self.orderAction = 1
                    waiter.orders_open.update({self: [0, 0, 0]})
        # HIER REIN: Danke sagen für geschenktes Glas?

        if waiter.orders_open != {} and waiter.serv_guest is not None and\
                waiter.text_count == 51 and self.text_count == 51:
            if self in waiter.orders_open.keys():
                if self.art == 'guest':
                    if waiter.orders_open[self][0] == 2:  # wenn der actioncounter des gastes  = 2 ist:
                        waiter.orders_open[self][1] = random.randint(1, 4)
                        self.text = str(random.choice(('Ich will ein ', 'Für mich ein ', 'Ich nehm ')) + str(
                            drinks[waiter.orders_open[self][1]][0]))
                        self.text_count = 0
                        waiter.orders_open[self][0] = 3

                    elif waiter.orders_open[self][0] == 3:
                        waiter.orders_open[self][0] = 4

                    elif waiter.orders_open[self][0] == 11:  # wenn der actioncounter des gastes  = 2 ist:
                        self.text = random.choice(('Dankoletti!', 'Merci  vielmals!', 'Na endlich!', 'Mhhh, lecker.'))
                        self.text_count = 0
                        waiter.orders_open[self][0] = 12

                if self.art == 'player':
                    if waiter.orders_open[self][0] == 2:  # wenn der actioncounter des gastes  = 2 ist:
                        self.orderAction = 5
                        waiter.orders_open[self][0] = 3

                    elif waiter.orders_open[self][0] == 3:
                        waiter.orders_open[self][0] = 3.2

                    elif waiter.orders_open[self][0] == 3.2:
                        self.text_count = 0
                        self.text = str(random.choice(('Ich will ein ', 'Für mich ein ', 'Ich nehm ')) + str(
                            drinks[waiter.orders_open[self][1]][0]))
                        waiter.orders_open[self][0] = 3.5

                    elif waiter.orders_open[self][0] == 3.5:
                        waiter.orders_open[self][0] = 4

                    elif waiter.orders_open[self][0] == 11:  # wenn der actioncounter des gastes  = 2 ist:
                        self.text = random.choice(('Dankoletti!', 'Merci  vielmals!', 'Na endlich!', 'Mhhh, lecker.'))
                        self.text_count = 0
                        waiter.orders_open[self][0] = 12

    def drink_a_sip(self, alc):
        self.sipCount = 0
        self.drunkenness += alc
        self.sips -= 1
        if self.drunkenness > 100:
            self.drunkenness = 100
        if self.drunkenness < 0:
            self.drunkenness = 0
