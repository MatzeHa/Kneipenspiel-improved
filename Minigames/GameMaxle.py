import pygame
import random
from Scripts.Util.ScaleImage import scale_image


def order_tuple(to_order):
    if to_order[0] < to_order[1]:
        t = (to_order[1], to_order[0])
        t = tuple(t)
    else:
        t = tuple(to_order)
    return t


pygame.init()

img_dice_cup = [pygame.image.load('../graph/games/cup.png'), pygame.image.load('../graph/games/cup_open.png')]
img_dice_cup = [scale_image(img, 120)[0] for img in img_dice_cup]
img_dice = [pygame.image.load('../graph/games/wurf1.png'), pygame.image.load('../graph/games/wurf2.png'),
            pygame.image.load('../graph/games/wurf3.png'), pygame.image.load('../graph/games/wurf4.png'),
            pygame.image.load('../graph/games/wurf5.png'), pygame.image.load('../graph/games/wurf6.png')]
img_dice = [scale_image(img, 50)[0] for img in img_dice]

img_Buttons = {"A": pygame.image.load('../graph/GUI/button_A.png'), "W": pygame.image.load('../graph/GUI/button_W.png')}
img_bg = pygame.image.load('../graph/games/holztisch.png')

font = pygame.font.SysFont('Courier', 30, True)
talk_font = pygame.font.SysFont('Courier', 20, True)

win_WIDTH = 1900 - 150 * 2
win_HEIGHT = 1068 - 150 * 2
win_SHIFTX = 150
win_SHIFTY = 150
SCALED_WIDTH = 150
OFFSET = 20

alc = 15

CUP_WIDTH = img_dice_cup[0].get_width()
CUP_HEIGHT = img_dice_cup[0].get_height()
BUTTON_WIDTH = img_Buttons["A"].get_width()
DICE_WIDTH = img_dice[0].get_width()
WAIT_TIME = 15
status_font = pygame.font.SysFont('Courier', 20, True)
bg_color = (50, 100, 100)

dice_order = {(-1, -1): -1, (2, 0): 0, (2, 1): 1, (3, 0): 2, (3, 1): 3, (3, 2): 4,
              (4, 0): 5, (4, 1): 6, (4, 2): 7, (4, 3): 8, (5, 0): 9,
              (5, 1): 10, (5, 2): 11, (5, 3): 12, (5, 4): 13, (0, 0): 14,
              (1, 1): 15, (2, 2): 16, (3, 3): 17, (4, 4): 18, (5, 5): 19,
              (1, 0): 20
              }


class GameMaxle:
    def __init__(self, guy, players, drinks):
        self.players = [guy] + players
        self.nr_players = len(self.players)
        self.points = [0 for i in range(0, self.nr_players)]
        self.cup_status = 0
        self.p_on_turn = -1
        self.portrait_h = 0
        self.portrait_w = 0
        self.text_h = 0

        self.drinks = drinks
        self.start_game = True

        self.WAIT_TIME = WAIT_TIME
        self.WAIT_TIME_PRAE = WAIT_TIME
        self.WAIT_TIME_POST = 0
        #        self.last_throw = (-1, -1)
        self.throw_dice = False
        self.thrown = False
        self.player_called = False
        self.doubt = False
        self.victory = 0
        self.first_round = True
        self.win = False

        self.call = (-1, -1)
        self.status = "Lets play Mäxle!"
        self.throw = (-1, -1)
        self.dice_call = [0, 0]
        self.win_copy = None
        self.dice_chose = 0
        self.show_dice = False
        self.do_action = None

    def draw_init(self, win):
        print("### MÄXLE ###")
        print(dice_order)
        self.cup_status = 0
        dirtyrect = pygame.Rect(win_SHIFTX, win_SHIFTY, win_WIDTH, win_HEIGHT)
        win.blit(img_bg, (dirtyrect.x, dirtyrect.y))
        # pygame.draw.rect(win, bg_color, dirtyrect)
        self.draw_portraits(win)
        if self.p_on_turn == 0:
            self.draw_help(win)
        self.win_copy = win.copy()
        return dirtyrect

    def do_turn(self, win):
        dirtyrects = []
        dirtyrects = dirtyrects + self.del_turn(win)

        if self.start_game:
            self.p_on_turn = 0  # TODO: randomisieren
            self.start_game = False

        if not self.victory:
            turn_valid = False
            if self.p_on_turn == 0:
                turn_valid = self.turn_player()
            elif self.WAIT_TIME == 0:
                turn_valid = self.turn_npc()
                self.WAIT_TIME = 50
            else:
                self.WAIT_TIME -= 1

            if turn_valid:
                self.next_player()

        else:
            if self.WAIT_TIME > 0:
                self.WAIT_TIME -= 1
            else:
                self.cup_status = 1
                self.check_victory()

        dirtyrects = dirtyrects + self.draw_turn(win)

        return dirtyrects

    def turn_player(self):
        turn_valid = False
        # throw dice
        # TODO: self.action anstatt self.trown, self.call ... = zusammenfassen
        if self.do_action == "dice":
            self.first_round = False
            if not self.thrown:
                if self.WAIT_TIME > 0:
                    self.WAIT_TIME -= 1
                    d1 = random.randint(0, 5)
                    d2 = random.randint(0, 5)
                    self.throw = (d1, d2)

                else:
                    self.cup_status = 1
                    self.do_action = "thrown"
                    self.WAIT_TIME = WAIT_TIME
                    self.status = "Du hast gewürfelt. (" + str(self.throw[0] + 1) + ", " + str(self.throw[1] + 1) + ")"
                    self.dice_call = [d for d in self.throw]
                    if dice_order[order_tuple(self.throw)] == 20:
                        self.victory = True
                        self.WAIT_TIME = WAIT_TIME

        elif self.do_action == "thrown":
            if self.player_called:
                # wenn wette gültig
                if self.call_valid():
                    self.call = self.dice_call
                    self.status = "Du bietest (" + str(self.call[0] + 1) + ", " + str(self.call[1] + 1) + ")"
                    self.player_called = False
                    self.do_action = None
                    turn_valid = True
                    self.do_action = None
                    self.cup_status = 0
                else:
                    self.status = "Ungültig, du musst höher bieten!"
                    self.player_called = False
        elif self.do_action == "doubt":
            if self.WAIT_TIME > 0:
                self.WAIT_TIME -= 1
                self.status = "Du zweifelst an. Wette war: " + str(self.call[0] + 1) + "," + str(self.call[1] + 1)
                self.cup_status = 1
            else:
                self.WAIT_TIME = WAIT_TIME
                self.show_dice = True
                self.victory = True

        return turn_valid

    def turn_npc(self):
        turn_valid = False
        if not self.do_action:
            if self.first_round:  # obsolet?
                self.first_round = False
                self.do_action = "dice"
            else:
                self.do_action = self.calc_throw_or_doubt()

        elif self.do_action == "dice":
            d1 = random.randint(0, 5)
            d2 = random.randint(0, 5)
            self.throw = (d1, d2)
            self.do_action = "call"
            self.status = "Spieler" + str(self.p_on_turn) + "hat gewürfelt.(" + \
                          str(self.throw[0] + 1) + ", " + str(self.throw[1] + 1) + ")"
            self.cup_status = 0
            self.do_action = "call"
            self.thrown = True
            if dice_order[order_tuple(self.throw)] == 20:
                self.victory = True
                self.WAIT_TIME = WAIT_TIME
        elif self.do_action == "call":
            if self.thrown:
                self.make_call()
                self.thrown = False
                self.cup_status = 0
                self.status = "Ich hab (" + str(self.call[0] + 1) + ", " + str(self.call[1] + 1) + ")"
            elif not self.thrown:
                turn_valid = True
                self.do_action = None

        elif self.do_action == "doubt":
            if not self.doubt:
                self.doubt = True
                self.status = "DAS BEZWEIFLE ICH STARK!"
                self.WAIT_TIME = WAIT_TIME
                self.cup_status = 1
            else:
                self.doubt = False
                self.victory = True
                self.do_action = "doubt"
                self.WAIT_TIME = WAIT_TIME
        return turn_valid

    def init_values(self):
        self.WAIT_TIME = WAIT_TIME
        self.WAIT_TIME_PRAE = WAIT_TIME
        self.WAIT_TIME_POST = 0
        self.throw_dice = False
        self.player_called = False
        self.doubt = False
        self.victory = False
        self.first_round = True
        self.call = (-1, -1)
        self.show_dice = False
        self.do_action = None
        self.win = False
        self.thrown = False
        self.cup_status = 0

    def calc_throw_or_doubt(self):
        if dice_order[order_tuple(self.call)] == 19 or dice_order[order_tuple(self.call)] == 19:
            r = "doubt"
        else:
            call_value = dice_order[order_tuple(self.call)]
            max_value = len(dice_order) - 2
            ratio = (call_value / max_value) ** 2
            rndm = random.random()
            if ratio < rndm:
                r = "dice"
            else:
                r = "doubt"
        return r

    def check_bet(self):
        dice_call = order_tuple(self.call)
        last_call = order_tuple(self.last_throw)
        if dice_order[dice_call] == dice_order[last_call]:
            return 1
        else:
            return 2

    def check_victory(self):
        if self.p_on_turn == 0:
            if self.do_action == "maxle":
                self.status = "Beginne neue Runde. Du fängst an."
                self.init_values()
            elif self.do_action == "lose":
                self.status = "Beginne neue Runde. Du fängst an."
                self.init_values()
            elif self.do_action == "win":
                self.last_player()
                self.status = "Beginne neue Runde. Spieler " + str(self.p_on_turn) + " fängt an."
                self.init_values()
            elif dice_order[order_tuple(self.throw)] == 20:
                self.do_action = "maxle"
                self.status = "Du hast ein Mäxle! Alle anderen verlieren. :D"
                self.points = [self.points[0]] + [self.points[i] + 1 for i in range(1, self.nr_players)]
                self.WAIT_TIME = WAIT_TIME

            if self.do_action == "doubt":
                throw = dice_order[order_tuple(self.throw)]
                call = dice_order[order_tuple(self.call)]
                if throw == call:
                    self.status = "Du verlierst."
                    self.do_action = "lose"
                    self.points[0] += 1
                    self.players[0].drink_a_sip(alc)
                    self.WAIT_TIME = WAIT_TIME
                else:
                    self.status = "Du gewinnst!"
                    self.do_action = "win"
                    self.points[self.nr_players - 1] += 1
                    self.players[self.nr_players - 1].drink_a_sip(alc)
                    self.WAIT_TIME = WAIT_TIME
        else:
            if self.do_action == "maxle":
                self.status = "Beginne neue Runde. Spieler " + str(self.p_on_turn) + " fängt an."
                self.init_values()

            elif self.do_action == "lose":
                self.status = "Beginne neue Runde. Spieler " + str(self.p_on_turn) + " fängt an."
                self.init_values()
            elif self.do_action == "win":
                self.last_player()
                self.status = "Beginne neue Runde. Spieler " + str(self.p_on_turn) + " fängt an."
                self.init_values()
            elif dice_order[order_tuple(self.throw)] == 20:
                self.do_action = "maxle"
                self.status = "Spieler " + str(self.p_on_turn) + " hat ein Mäxle! Alle anderen verlieren. X("
                self.points = [self.points[i] + 1 if i != self.p_on_turn
                               else self.points[i] for i in range(0, self.nr_players)]
                self.WAIT_TIME = WAIT_TIME
            if self.do_action == "doubt":
                throw = dice_order[order_tuple(self.throw)]
                call = dice_order[order_tuple(self.call)]
                if throw == call:
                    self.status = "Spieler " + str(self.p_on_turn) + " verliert."
                    self.do_action = "lose"
                    self.points[self.p_on_turn] += 1
                    self.players[self.p_on_turn].drink_a_sip(alc)
                    self.WAIT_TIME = WAIT_TIME
                else:
                    self.status = "Spieler " + str(self.p_on_turn) + " gewinnt!"
                    self.do_action = "win"
                    self.points[self.nr_players - 1] += 1
                    self.players[self.p_on_turn - 1].drink_a_sip(alc)
                    self.WAIT_TIME = WAIT_TIME

    def call_valid(self):
        dice_call = order_tuple(self.dice_call)
        last_call = order_tuple(self.call)
        if dice_order[dice_call] > dice_order[last_call]:
            return True
        else:
            return False

    def make_call(self):
        possible_keys = []
        call = order_tuple(self.call)
        for key in dice_order.keys():
            key = order_tuple(key)
            if dice_order[key] > dice_order[call] and dice_order[key] != 20:
                possible_keys.append(key)
        if not possible_keys:
            self.victory = True
            self.WAIT_TIME = WAIT_TIME
        else:
            throw_inside = False
            for i in possible_keys:
                if order_tuple(self.throw) == i:
                    throw_inside = True
            if throw_inside:
                stay = 75 + random.randint(-20, 10)
                high = 100 - stay * 1 / 3
            else:
                stay = 85 + random.randint(0, 5)
                low = -1
                high = 100 - stay
            rndm = random.randint(0, 100)
            if high < rndm:
                call_list = [t for t in possible_keys
                             if dice_order[order_tuple(t)] > dice_order[order_tuple(self.throw)]]
                self.call = random.choice(call_list)
            elif stay > rndm:
                self.call = self.throw

            else:
                call_list = [t for t in possible_keys
                             if dice_order[order_tuple(t)] < dice_order[order_tuple(self.throw)]]
                self.call = random.choice(call_list)

    def del_turn(self, win):
        dirtyrects = []
        dirtyrects = dirtyrects + [self.del_status(win)]
        dirtyrects = dirtyrects + [self.del_drunkenness(win)]
        dirtyrects = dirtyrects + [self.del_dice(win)]
        dirtyrects = dirtyrects + [self.del_cup(win)]
        dirtyrects = dirtyrects + [self.del_call_dice(win)]
        dirtyrects = dirtyrects + [self.del_help(win)]
        return dirtyrects

    def draw_turn(self, win):
        dirtyrects = []
        dirtyrects = dirtyrects + [self.draw_status(win)]
        dirtyrects = dirtyrects + self.draw_drunkenness(win)
        if self.cup_status == 0:
            dirtyrects = dirtyrects + [self.draw_dice(win)]
            dirtyrects = dirtyrects + [self.draw_cup(win)]
        else:
            dirtyrects = dirtyrects + [self.draw_cup(win)]
            dirtyrects = dirtyrects + [self.draw_dice(win)]
        if self.p_on_turn == 0:
            if not self.do_action:
                dirtyrects = dirtyrects + [self.draw_help(win)]
            if self.do_action == "thrown":
                dirtyrects = dirtyrects + [self.draw_call_dice(win)]
        return dirtyrects

    def incr_dice(self):
        self.dice_call[self.dice_chose] += 1
        if self.dice_call[self.dice_chose] == 6:
            self.dice_call[self.dice_chose] = 5

    def decr_dice(self):
        self.dice_call[self.dice_chose] -= 1
        if self.dice_call[self.dice_chose] == -1:
            self.dice_call[self.dice_chose] = 0

    def draw_drunkenness(self, win):
        bar_height = 32
        dirtyrects = []
        dirtyrect = pygame.Rect(win_SHIFTX + win_WIDTH / 2 - SCALED_WIDTH / 2,
                                win_SHIFTY + win_HEIGHT - self.text_h - bar_height,
                                self.portrait_w, bar_height)
        pygame.draw.rect(win, (150, 150, 150), (dirtyrect.x, dirtyrect.y, self.portrait_w, bar_height), 0)
        pygame.draw.rect(win, self.players[0].dispcol,
                         (dirtyrect.x, dirtyrect.y + 3,
                          self.portrait_w / 100 * self.players[0].drunkenness, bar_height - 6), 0)
        for i in range(0, 10):
            pygame.draw.rect(win, (10, 10, 10), (dirtyrect.x + i * 15, dirtyrect.y + 2,
                                                 15, bar_height - 4), 2)
        dirtyrects.extend([dirtyrect])
        for p in range(1, self.nr_players):
            x_shift = win_WIDTH / self.nr_players
            dirtyrect = pygame.Rect(win_SHIFTX + x_shift * p - SCALED_WIDTH / 2,
                                    win_SHIFTY + self.portrait_h + self.text_h - bar_height,
                                    self.portrait_w, bar_height)
            pygame.draw.rect(win, (150, 150, 150), (dirtyrect.x, dirtyrect.y, self.portrait_w, bar_height), 0)
            pygame.draw.rect(win, self.players[p].dispcol,
                             (dirtyrect.x, dirtyrect.y + 3,
                              self.portrait_w / 100 * self.players[p].drunkenness, bar_height - 6), 0)
            for i in range(0, 10):
                pygame.draw.rect(win, (10, 10, 10), (dirtyrect.x + i * 15, dirtyrect.y + 2,
                                                     15, bar_height - 4), 2)

            dirtyrects.extend([dirtyrect])

        return dirtyrects

    def del_drunkenness(self, win):
        bar_height = 32
        dirtyrects = pygame.Rect(win_SHIFTX + win_WIDTH / 2 - SCALED_WIDTH / 2,
                                 win_SHIFTY + win_HEIGHT - self.text_h - bar_height,
                                 self.portrait_w, bar_height)
        win.blit(self.win_copy, (dirtyrects.x, dirtyrects.y), dirtyrects)
        return dirtyrects

    def draw_call_dice(self, win):
        space = 25
        dirtyrect = pygame.Rect(win_SHIFTX + 1300, win_SHIFTY + 600, DICE_WIDTH * 2 + space, DICE_WIDTH)
        win.blit(img_dice[self.dice_call[0]], (dirtyrect.x, dirtyrect.y))
        win.blit(img_dice[self.dice_call[1]], (DICE_WIDTH + space + dirtyrect.x, dirtyrect.y))
        if self.dice_chose == 0:
            pygame.draw.rect(win, (255, 200, 0), (win_SHIFTX + 1300, win_SHIFTY + 600, DICE_WIDTH, DICE_WIDTH), 5)
        else:
            pygame.draw.rect(win, (255, 200, 0), (win_SHIFTX + 1300 + space + DICE_WIDTH,
                                                  win_SHIFTY + 600, DICE_WIDTH, DICE_WIDTH), 5)
        return dirtyrect

    def del_call_dice(self, win):
        space = 25
        dirtyrect = pygame.Rect(win_SHIFTX + 1300, win_SHIFTY + 600, DICE_WIDTH * 2 + space, DICE_WIDTH)
        #        pygame.draw.rect(win, bg_color, dirtyrect)
        win.blit(self.win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        return dirtyrect

    def draw_status(self, win):
        dirtyrect = pygame.Rect(win_SHIFTX + int(win_WIDTH * 0.58), (win_SHIFTY + win_HEIGHT - self.text_h * 2),
                                int(win_WIDTH * 0.42) - OFFSET, 50)
        dirtyrect2 = pygame.Rect(dirtyrect.x - 2, dirtyrect.y - 2, 500 + 2 * 2, 50 + 2 * 2)
        pygame.draw.rect(win, (7, 7, 7), dirtyrect2)
        pygame.draw.rect(win, (235, 138, 4), dirtyrect)
        text = status_font.render(self.status, 1, (0, 0, 0))
        win.blit(text, (win_SHIFTX + int(win_WIDTH * 0.58) + OFFSET, (win_SHIFTY + win_HEIGHT - self.text_h * 2 + 10)))
        return dirtyrect

    def del_status(self, win):
        dirtyrect = pygame.Rect(win_SHIFTX + int(win_WIDTH * 0.58), (win_SHIFTY + win_HEIGHT - self.text_h * 2),
                                int(win_WIDTH * 0.42) - OFFSET, 50)
        dirtyrect = pygame.Rect(dirtyrect.x - 2, dirtyrect.y - 2, 500 + 2 * 2, 50 + 2 * 2)
        pygame.draw.rect(win, bg_color, dirtyrect)
        win.blit(self.win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        return dirtyrect

    def draw_help(self, win):
        dirtyrect = pygame.Rect(win_SHIFTX + 50, win_SHIFTY + win_HEIGHT - BUTTON_WIDTH * 2 - OFFSET,
                                BUTTON_WIDTH, BUTTON_WIDTH * 2)
        if self.p_on_turn == 0 and not self.do_action:
            win.blit(img_Buttons["W"], (dirtyrect.x, dirtyrect.y))
            win.blit(img_Buttons["A"], (dirtyrect.x, dirtyrect.y + BUTTON_WIDTH))
            text = "Würfeln"
            text_rendered = font.render(text, 0, (0, 0, 0))
            win.blit(text_rendered, (dirtyrect.x + BUTTON_WIDTH, dirtyrect.y + 25))
            text = "Anzweifeln"
            text_rendered = font.render(text, 0, (0, 0, 0))
            # w, h = font.size(text)
            w = 400
            win.blit(text_rendered, (dirtyrect.x + BUTTON_WIDTH, dirtyrect.y + BUTTON_WIDTH + 25))
            dirtyrect = pygame.Rect(win_SHIFTX + 50, win_SHIFTY + 500, BUTTON_WIDTH + w, BUTTON_WIDTH * 2)
        return dirtyrect

    def del_help(self, win):
        dirtyrect = pygame.Rect(win_SHIFTX + 50, win_SHIFTY + win_HEIGHT - BUTTON_WIDTH * 2 - OFFSET,
                                BUTTON_WIDTH + 400, BUTTON_WIDTH * 2)
        win.blit(self.win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        return dirtyrect

    def draw_cup(self, win):
        if self.p_on_turn == 0:
            dirtyrect = pygame.Rect(win_SHIFTX + int(win_WIDTH / 2) - CUP_WIDTH / 2, win_SHIFTY + win_HEIGHT -
                                    self.text_h - self.portrait_h - CUP_HEIGHT, CUP_WIDTH, CUP_HEIGHT)
        else:
            x_shift = win_WIDTH / self.nr_players
            dirtyrect = pygame.Rect(win_SHIFTX + x_shift * self.p_on_turn - CUP_WIDTH / 2,
                                    win_SHIFTY + self.portrait_h +
                                    self.text_h, CUP_WIDTH, CUP_HEIGHT)
        win.blit(img_dice_cup[self.cup_status], (dirtyrect.x, dirtyrect.y))
        return dirtyrect

    def del_cup(self, win):
        if self.p_on_turn == 0:
            dirtyrect = pygame.Rect(win_SHIFTX + int(win_WIDTH / 2) - CUP_WIDTH / 2, win_SHIFTY + win_HEIGHT -
                                    self.text_h - self.portrait_h - CUP_HEIGHT, CUP_WIDTH, CUP_HEIGHT)
        else:
            x_shift = win_WIDTH / self.nr_players
            dirtyrect = pygame.Rect(win_SHIFTX + x_shift * self.p_on_turn - CUP_WIDTH / 2,
                                    win_SHIFTY + self.portrait_h +
                                    self.text_h, CUP_WIDTH, CUP_HEIGHT)
        win.blit(self.win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        return dirtyrect

    def draw_dice(self, win):
        if self.p_on_turn == 0:
            dirtyrect = pygame.Rect(win_SHIFTX + int(win_WIDTH / 2) - DICE_WIDTH, win_SHIFTY + win_HEIGHT -
                                    self.portrait_h - self.text_h - DICE_WIDTH * 0.7, DICE_WIDTH * 2, DICE_WIDTH)
            if self.throw:
                win.blit(img_dice[self.throw[0]], (win_SHIFTX + int(win_WIDTH / 2) - DICE_WIDTH, dirtyrect.y))
                win.blit(img_dice[self.throw[1]], (win_SHIFTX + int(win_WIDTH / 2), dirtyrect.y))
        else:
            x_shift = win_WIDTH / self.nr_players
            dirtyrect = pygame.Rect(win_SHIFTX + x_shift * self.p_on_turn - DICE_WIDTH, win_SHIFTY + self.portrait_h +
                                    self.text_h + int(CUP_HEIGHT * 0.60), DICE_WIDTH * 2, DICE_WIDTH)
            if self.throw:
                win.blit(img_dice[self.throw[0]], (dirtyrect.x, dirtyrect.y))
                win.blit(img_dice[self.throw[1]], (dirtyrect.x + DICE_WIDTH, dirtyrect.y))
        return dirtyrect

    def del_dice(self, win):
        if self.p_on_turn == 0:
            dirtyrect = pygame.Rect(win_SHIFTX + int(win_WIDTH / 2) - DICE_WIDTH, win_SHIFTY + win_HEIGHT -
                                    self.portrait_h - self.text_h - DICE_WIDTH * 0.7, DICE_WIDTH * 2, DICE_WIDTH)
        else:
            x_shift = win_WIDTH / self.nr_players
            dirtyrect = pygame.Rect(win_SHIFTX + x_shift * self.p_on_turn - DICE_WIDTH, win_SHIFTY + self.portrait_h +
                                    self.text_h + int(CUP_HEIGHT * 0.60), DICE_WIDTH * 2, DICE_WIDTH)
        win.blit(self.win_copy, (dirtyrect.x, dirtyrect.y), dirtyrect)
        return dirtyrect

    def draw_portraits(self, win):
        self.portrait_w = 150
        portrait_scaled, self.portrait_h = scale_image(self.players[0].portrait, self.portrait_w)
        text = self.players[0].name
        text_rendered = font.render(text, 0, self.players[0].textcolor)
        text_w, self.text_h = font.size(text)
        win.blit(text_rendered, (win_SHIFTX + win_WIDTH / 2 - text_w / 2, win_SHIFTY + win_HEIGHT - self.text_h))
        win.blit(portrait_scaled, (win_SHIFTX + win_WIDTH / 2 - SCALED_WIDTH / 2, win_SHIFTY + win_HEIGHT -
                                   self.portrait_h - self.text_h))
        for p in range(1, self.nr_players):
            portrait_scaled = scale_image(self.players[p].portrait, 150)[0]
            portrait_h = portrait_scaled.get_height()
            text = self.players[p].name
            text_rendered = font.render(text, 0, self.players[p].textcolor)
            text_w, self.text_h = font.size(text)
            x_shift = win_WIDTH / self.nr_players
            win.blit(text_rendered, (win_SHIFTX + x_shift * p - text_w / 2, win_SHIFTY))
            win.blit(portrait_scaled, (win_SHIFTX + x_shift * p - SCALED_WIDTH / 2, win_SHIFTY + self.text_h))

    def last_player(self):
        self.p_on_turn -= 1
        if self.p_on_turn == -1:
            self.p_on_turn = self.nr_players - 1

    def next_player(self):
        self.p_on_turn += 1
        if self.p_on_turn == self.nr_players:
            self.p_on_turn = 0


