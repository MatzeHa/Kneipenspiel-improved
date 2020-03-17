import pygame
from types import MethodType
pygame.init()


class PauseMenu:
    def __init__(self, win, setup):
        win_size = pygame.display.get_surface().get_size()
        self.win = win
        self.setup = setup
        self.win_width, self.win_height = win_size

        self.active = False
        self.start_pause = False
        self.end_pause = False
        self.quit = False

        self.menu_size = (self.win_width * (1 / 5), self.win_height * (1 / 8), self.win_width * (3 / 5),
                          self.win_height * (6 / 8))
        self.dirtyrect = pygame.Rect(self.menu_size)
        self.pos_x = self.win_width * (1 / 5)
        self.pos_y = self.win_height * (1 / 8)

        self.bar_pos = (self.win_width * (3 / 10), self.win_height * (2 / 8),
                        self.win_width*(4/10), self.win_height * (1 / 32))
#        self.win = pygame.Surface(win_size)

        self.nr_selectables = [1, 1, 1, 1, 1]
        self.selected = [1, 0, 0, 0, 0]
        self.select_pos = [self.win_width * (3 / 10), self.win_height * (2 / 8),
                           self.win_width*(4/10), self.win_height * (1 / 32)]

        self.screen = "pause_menu"

        self.options = {"bgcol": (0, 0, 0)}

        self.font = pygame.font.SysFont('Courier', 16, True)

        but1 = self.Button(self.bar_pos, "Weiter", self.font, (0, 4), self.menu_size)
        but1.fun = MethodType(self.end_pause_fun, but1)
        but2 = self.Button(self.bar_pos, "Optionen", self.font, (1, 4), self.menu_size)
        but2.fun = MethodType(self.options_fun, but2)
        but3 = self.Button(self.bar_pos, "Hilfe", self.font, (2, 4), self.menu_size)
        but3.fun = MethodType(self.help_fun, but3)
        but4 = self.Button(self.bar_pos, "Grafik", self.font, (3, 4), self.menu_size)
        but4.fun = MethodType(self.graphics_fun, but4)
        but5 = self.Button(self.bar_pos, "Beenden", self.font, (4, 4), self.menu_size)
        but5.fun = MethodType(self.quit_fun, but5)

        but10 = self.Button(self.bar_pos, "option 1", self.font, (0, 4), self.menu_size)
        but10.fun = MethodType(self.options1_fun, but10)
        but11 = self.Button(self.bar_pos, "option 2", self.font, (1, 4), self.menu_size)
        but11.fun = MethodType(self.pause_fun, but11)
        but12 = self.Button(self.bar_pos, "option 3", self.font, (2, 4), self.menu_size)
        but12.fun = MethodType(self.pause_fun, but12)
        but13 = self.Button(self.bar_pos, "option 4", self.font, (3, 4), self.menu_size)
        but13.fun = MethodType(self.pause_fun, but13)
        but14 = self.Button(self.bar_pos, "Zurück", self.font, (4, 4), self.menu_size)
        but14.fun = MethodType(self.pause_fun, but14)

        but100 = self.Button(self.bar_pos, "suboption 1", self.font, (0, 6), self.menu_size)
        but100.fun = MethodType(self.options_fun, but100)
        but101 = self.Button(self.bar_pos, "suboption 2", self.font, (1, 6), self.menu_size)
        but101.fun = MethodType(self.options_fun, but101)
        but102 = self.Button(self.bar_pos, "suboption 3", self.font, (2, 6), self.menu_size)
        but102.fun = MethodType(self.options_fun, but102)
        but103 = self.Button(self.bar_pos, "suboption 4", self.font, (3, 6), self.menu_size)
        but103.fun = MethodType(self.options_fun, but103)
        but104 = self.Button(self.bar_pos, "suboption 5", self.font, (4, 6), self.menu_size)
        but104.fun = MethodType(self.options_fun, but104)
        but105 = self.Button(self.bar_pos, "suboption 6", self.font, (5, 6), self.menu_size)
        but105.fun = MethodType(self.options_fun, but105)
        but106 = self.Button(self.bar_pos, "Zurück", self.font, (6, 6), self.menu_size)
        but106.fun = MethodType(self.options_fun, but106)

        but20 = self.Button(self.bar_pos, "Zurück", self.font, (4, 4), self.menu_size)
        but20.fun = MethodType(self.pause_fun, but20)

        sli30 = self.Slider(self.bar_pos, (1, 0, 0), (0, 4), self.menu_size)
        sli30.fun = MethodType(self.pause_fun, sli30)
        sli31 = self.Slider(self.bar_pos, (0, 1, 0), (1, 4), self.menu_size)
        sli31.fun = MethodType(self.pause_fun, sli31)
        sli32 = self.Slider(self.bar_pos, (0, 0, 1), (2, 4), self.menu_size)
        sli32.fun = MethodType(self.pause_fun, sli32)
        dis33 = self.Display(self.bar_pos, (3, 4), self.menu_size)
        but34 = self.Button(self.bar_pos, "Zurück", self.font, (4, 4), self.menu_size)
        but34.fun = MethodType(self.pause_fun, but34)

        but40 = self.Button(self.bar_pos, "Zurück", self.font, (1, 3), self.menu_size)
        but40.fun = MethodType(self.pause_fun, but40)
        but41 = self.Button(self.bar_pos, "Beenden", self.font, (2, 3), self.menu_size)
        but41.fun = MethodType(self.really_quit_fun, but41)

        self.clickables = {"pause_menu": [but1, but2, but3, but4, but5],
                           "options": [but10, but11, but12, but13, but14],
                           "options1": [but100, but101, but102, but103, but104, but105, but106],
                           "help": [0, 0, 0, 0, but20],
                           "graphics": [sli30, sli31, sli32, dis33, but34],
                           "quit": [0, but40, but41, 0]}

    def check_action(self, win, lvl):
        if self.start_pause:
            dirtyrects = self.dirtyrect
            self.start_pause_fun(win, lvl)
            self.start_pause = False

        elif self.end_pause:
            dirtyrects = self.dirtyrect
            # setup.update_bg(win)
            self.reset_pause_menu()
            win.blit(lvl.win_copy_change_mode, (0, 0))

        else:
            dirtyrects = self.blitten()
        return dirtyrects

    def pause_fun(self, x):
        self.screen = "pause_menu"
        self.nr_selectables = [1, 1, 1, 1, 1]
        self.selected = [1, 0, 0, 0, 0]
        return True

    def blit_pause(self):
        for i in self.clickables["pause_menu"]:
            i.blit_button(self.win, self.selected[i.nr])


    def quit_fun(self, x):
        self.screen = "quit"
        self.nr_selectables = [0, 1, 1, 0]
        self.selected = [0, 1, 0, 0]
        return self.selected

    def blit_quit(self):
        for i in self.clickables["quit"]:
            if isinstance(i, self.Button):
                i.blit_button(self.win, self.selected[i.nr])

    def really_quit_fun(self, x):
        self.quit = True

    def reset_pause_menu(self):
        self.screen = "pause_menu"
        self.dirtyrect = pygame.Rect(self.win_width * (1 / 5), self.win_height * (1 / 8), self.win_width * (3 / 5),
                                     self.win_height * (6 / 8))
        self.end_pause = False
        pygame.mouse.set_visible(False)
        self.active = False

    def start_pause_fun(self, win, lvl):
        lvl.win_copy_change_mode = win.copy()

    def end_pause_fun(self, x):
        self.set_bgcolor()
        self.end_pause = True
        self.dirtyrect = pygame.Rect(0, 0, self.win_width, self.win_height)
        pygame.mouse.set_visible(True)

    def set_bgcolor(self):
        self.options["bgcol"] = self.get_bgcolor()

    def get_bgcolor(self):
        r = self.clickables["graphics"][0].val
        g = self.clickables["graphics"][1].val
        b = self.clickables["graphics"][2].val
        return r, g, b


    def options_fun(self, x):
        self.screen = "options"
        self.nr_selectables = [1, 1, 1, 1, 1]
        self.selected = [1, 0, 0, 0, 0]

    def blit_options(self):
        for i in self.clickables["options"]:
            i.blit_button(self.win, self.selected[i.nr])

    def options1_fun(self, x):
        self.screen = "options1"
        self.nr_selectables = [1, 1, 1, 1, 1, 1, 1]
        self.selected = [1, 0, 0, 0, 0, 0, 0]
        return self.selected

    def blit_options1(self):
        for i in self.clickables["options1"]:
            i.blit_button(self.win, self.selected[i.nr])


    def help_fun(self, x):
        self.screen = "help"
        self.nr_selectables = [0, 0, 0, 0, 1]
        self.selected = [0, 0, 0, 0, 1]

    def blit_help(self):
        self.selected = [0, 0, 0, 0, 1]
        for i in self.clickables["help"]:
            if isinstance(i, self.Button):
                i.blit_button(self.win, self.selected[i.nr])

    def graphics_fun(self, x):
        self.screen = "graphics"
        self.nr_selectables = [1, 1, 1, 0, 1]
        self.selected = [1, 0, 0, 0, 0]

    def blit_graphics(self):
        for i in self.clickables["graphics"]:
            if isinstance(i, self.Button) or isinstance(i, self.Slider):
                i.blit_button(self.win, self.selected[i.nr])
            if isinstance(i, self.Display):
                i.blit_button(self.win, self.get_bgcolor())


    def do_action(self, key):
        clickables = self.clickables[self.screen]
        nr = -1
        for i in self.selected:
            nr += 1
            if i:
                clickables[nr].fun()

    def do_action_mouse(self, mouse_pos, button):
        sel = []
        selection = []
        for i in self.clickables[self.screen]:
            if isinstance(i, self.Button) or isinstance(i, self.Slider):
                if i.pos[0] < mouse_pos[0] < i.pos[0] + i.pos[2]:
                    if i.pos[1] < mouse_pos[1] < i.pos[1] + i.pos[3]:
                        sel.append(1)
                        if button[0]:
                            if isinstance(i, self.Button):
                                selection = i.fun()
                            elif isinstance(i, self.Slider):
                                i.click(mouse_pos)
                    else:
                        sel.append(0)
            else:
                sel.append(0)

        if not selection:
            if sum(sel):
                self.selected = sel


    def blitten(self):
        pygame.mouse.set_visible(True)
        self.win.fill((0, 0, 255), self.dirtyrect)
        if self.screen == "pause_menu":
            self.blit_pause()
        elif self.screen == "options":
            self.blit_options()
        elif self.screen == "options1":
            self.blit_options1()
        elif self.screen == "help":
            self.blit_help()
        elif self.screen == "graphics":
            self.blit_graphics()
        elif self.screen == "quit":
            self.blit_quit()
        return self.dirtyrect


    class Display:
        def __init__(self, pos, nr, menu_size):
            self.nr = nr[0]
            self.pos = list(pos)
            y = menu_size[1] + ((nr[0]+1)/(nr[1]+2)) * menu_size[3] - (self.pos[3]/2)
            self.pos[1] = y
            self.selected = False

        def blit_button(self, win, color):
            pygame.draw.rect(win, color, self.pos)
            pygame.draw.rect(win, (0, 0, 0), self.pos, 2)

    class Button:
        def __init__(self, pos, caption, font, nr, menu_size):
            self.nr = nr[0]
            self.pos = list(pos)
            y = menu_size[1] + ((nr[0]+1)/(nr[1]+2)) * menu_size[3] - (self.pos[3]/2)
            self.pos[1] = y
            self.text = font.render(caption, 1, (0, 0, 0))
            self.selected = False

        def blit_button(self, win, selected):
            pygame.draw.rect(win, (80, 80, 80), self.pos)
            pygame.draw.rect(win, (0, 0, 0), self.pos, 2)
            win.blit(self.text, (self.pos[0] + (self.pos[2] / 100), self.pos[1] + (self.pos[3] / 200)))
            if selected:
                pygame.draw.rect(win, (80, 255, 255), self.pos, 2)

    class Slider:
        def __init__(self, pos, color, nr, menu_size):
            self.nr = nr[0]
            self.pos = list(pos)
            y = menu_size[1] + ((nr[0] + 1) / (nr[1] + 2)) * menu_size[3] - (self.pos[3] / 2)
            self.pos[1] = y
            self.selected = False
            self.intervall = pos[2] / 255
            self.color = color
            self.val = 0

        def blit_button(self, win, selected):
            pos_draw = self.pos.copy()
            pos_draw[2] = self.intervall + 1
            for i in range(0, 255):
                pygame.draw.rect(win, (i*self.color[0], i*self.color[1], i*self.color[2]), pos_draw)
                pos_draw[0] = self.intervall + pos_draw[0]
            pygame.draw.rect(win, (0, 0, 0), self.pos, 2)
            pointer_pos = self.pos.copy()
            pointer_pos[0] = pointer_pos[0] + self.intervall*self.val - 3
            pointer_pos[2] = 6
            pygame.draw.rect(win, (255, 255, 255), pointer_pos, 1)

            if selected:
                pygame.draw.rect(win, (80, 255, 255), self.pos, 2)

        def click(self, mouse_pos):
            self.val = (mouse_pos[0] - self.pos[0])/self.intervall


