import pygame
import random
import Scripts.Util.DialogScript as DialogSkript

pygame.init()

font = pygame.font.SysFont('Courier', 30, True)
talk_font = pygame.font.SysFont('Courier', 20, True)
order_font = pygame.font.SysFont('Courier', 30, True)
order_choose_font = pygame.font.SysFont('Courier', 30, True)
# order_choose_font.set_italic(0)
text_mod = 0.5  # text-geschwindigkeits-modifikator


class DialogMenue:
    def __init__(self, win_sizex, win_sizey, surf_dialog, char):
        self.active = False

        self.surf = surf_dialog
        self.x_t1 = win_sizex * 0.05  # x_t1 =x.Koordinate von Talker 1
        self.y_t1 = win_sizey * 0.05
        self.w_t1 = char.portrait.get_width()
        self.h_t1 = char.portrait.get_height()

        self.x_t2 = win_sizex * 0.95 - char.portrait.get_width()  # x_t1 =x.Koordinate von Talker 2
        self.y_t2 = win_sizey * 0.05
        self.w_t2 = char.portrait.get_width()
        self.h_t2 = char.portrait.get_height()

        self.x_window = win_sizex * 0.05  # x_t1 =x.Koordinate von Dialodfenster
        self.y_window = win_sizey * 0.65  # x_t1 =x.Koordinate von Talker 1
        self.w_window = win_sizex * 0.9
        self.h_window = win_sizey * 0.3
        self.textCount = 0
        self.dirtyrects = []

        self.blit_first = True
        self.surf.fill((255, 130, 0))
        #        self.surf.fill((0,255,0))
        self.surf.set_alpha(200)

        self.chars = [char, char, None]
        self.dlst = []
        self.choice = 0
        self.char_talking = 1
        self.Line = 1  # startZeile

        border = 7
        pygame.draw.rect(self.surf, (5, 5, 5), (self.x_window, self.y_window, self.w_window - 1, self.h_window - 1),
                         border)

    def draw(self, win, win_copy_order):
        if not self.chars[2]:
            self.dlst = DialogSkript.Dialoge['ST_' + str(self.chars[self.char_talking].version)]
        else:
            self.dlst = DialogSkript.Triloge['ST_' + str(1)]
        # wenn irgendeine Zeile ausser der 0 kommt:
        if self.Line != 0:
            if isinstance(self.Line, tuple):
                self.Line = random.choice(self.Line)
            if self.dlst[self.Line][0] != 0:
                self.char_talking = self.dlst[self.Line][0]

            self.dirtyrects = []

            self.dirtyrects.append(pygame.Rect(self.x_t1, self.y_t1, self.w_t1, self.h_t1))
            self.dirtyrects.append(pygame.Rect(self.x_t2, self.y_t2, self.w_t2, self.h_t2))
            self.dirtyrects.append(pygame.Rect(self.x_window, self.y_window, self.w_window, self.h_window))
            win.blit(win_copy_order, (0, 0))
            win.blit(self.chars[0].portrait, (self.x_t1, self.y_t1), (0, 0, self.w_t1, self.h_t1))
            win.blit(self.chars[self.char_talking].portrait, (self.x_t2, self.y_t2), (0, 0, self.w_t2, self.h_t2))
            win.blit(self.surf, self.dirtyrects[2], self.dirtyrects[2])

            # Wenn Tuple (=Multiple Choice)
            if isinstance(self.dlst[self.Line][1], tuple):
                for i in range(0, len(self.dlst[self.Line][1])):
                    if i == self.choice:
                        text = order_font.render(str(self.dlst[self.Line][1][i]), 1, self.chars[0].textcolor)
                        win.blit(text, (self.x_window + 100, self.y_window + 50 + 50 * i))
                    else:
                        text = order_font.render(str(self.dlst[self.Line][1][i]), 0,
                                                 (int(round(self.chars[0].textcolor[0] * 0.2)),
                                                  int(round(self.chars[0].textcolor[1] * 0.2)),
                                                  int(round(self.chars[0].textcolor[2] * 0.2))))
                        win.blit(text, (self.x_window + 100, self.y_window + 50 + 50 * i))

            # Wenn String: Nur text blitten
            elif isinstance(self.dlst[self.Line][1], str):
                lenstr = len(str(self.dlst[self.Line][1])) + 30
                if lenstr < 50:
                    lenstr = 60
                if self.textCount < lenstr * text_mod:
                    textbg = order_choose_font.render(str(self.dlst[self.Line][1]), 1, (10, 10, 10))
                    win.blit(textbg, (self.x_window + round((self.w_window / 2) - (textbg.get_width() / 2)),
                                      self.y_window + 50))
                    text = order_font.render(str(self.dlst[self.Line][1]), 1,
                                             self.chars[self.dlst[self.Line][0]].textcolor)
                    win.blit(text, (self.x_window + round((self.w_window / 2) - (text.get_width() / 2)),
                                    self.y_window + 50))
                    self.textCount += 1
                else:
                    self.Line = self.dlst[self.Line][2]
                    self.textCount = 0

        # sonst: zurücksetzen
        else:
            self.Line = 1
            self.chars[0].talk_action = 3

        return self.dirtyrects

    def check_action(self, win, setup, g, lvl):
        dirtyrects = []
        if g.guy.talk_action == 2:  # besser: if dialog_menu.active:
            dirtyrects = g.dialog_menue.draw(win, lvl.sv["win_copy_change_mode"])

        elif g.guy.talk_action == 3:  # besser: if dialog_menu.active:
            g.dialog_menue.active = False
            g.guy.talk_action = 0
            dirtyrects = pygame.Rect(0, 0, setup.win_w, setup.win_h)
            win.blit(lvl.sv["win_copy"], (0, 0))
        return dirtyrects
