
class IncreaseI:
    def __init__(self):
        self.i = -1

    def increase(self):
        self.i += 1
        return self.i


def get_coords(win_w, wall_w, _cell_size):
    cell_size = _cell_size
    coord = []
#    if wall_h > wall_w:
#    win_w = win_h
#    wall_w = wall_h
    for crd in range(0, 1 + int((win_w - (wall_w*2)) / cell_size)):  # +1 weil tür an wand
        coord.append(wall_w + crd * cell_size)
    return coord


def get_max_coord(coord):
    if len(coord["w"]) < len(coord["h"]):
        max_coord = "h"
    else:
        max_coord = "w"
    return max_coord


class Raster:
    def __init__(self, win, wall_w, wall_h, cell_size):
        self.win_w, self.win_h = win.get_size()

        self.space_h = (self.win_w - 2 * wall_w - 1) // cell_size
        self.space_v = (self.win_h - 2 * wall_h - 1) // cell_size
        self.wall_w = wall_w
        self.wall_h = wall_h

    def draw(self, win):
        import pygame
        font = pygame.font.SysFont('Courier', 30, True)

        # quadrate:
        for i in range(0, self.space_h + 1):
            for j in range(0, self.space_v + 1):
                text = font.render(str(j) + "," + str(i), 1, (0, 0, 0))
                win.blit(text, (self.wall_w + i * 64, self.wall_h + j * 64))
        # senkrecht:
        for i in range(0, self.space_h + 1):
            pygame.draw.line(win, (0, 0, 0), (self.wall_w + i * 64, self.wall_h),
                             (self.wall_w + i * 64, self.win_h - self.wall_h))
        # waagrecht:
        for i in range(0, self.space_v + 1):
            pygame.draw.line(win, (0, 0, 0), (self.wall_w, self.wall_h + i * 64),
                             (self.win_w - self.wall_w, self.wall_h + i * 64))


class global_var:
    def __init__(self, setup):

        import pygame
        from Scripts.GameModes.Dialog import DialogMenue
        from Scripts.GameModes.Order import OrderMenue
        pygame.init()


        # drinks: Nr. : ('Name', Preis, Alkoholgehalt. # ?Anzahl der Schlücke? #
        # TODO: hier scheint noch ein bug zu sein,
        # wenn man das zweite getränk bestellt(?) hat man mehr (doppelt so viele?) schlücke
        drinks = {0: ("", 0, 0, 0), 1: ("Bier", 3, 10, 10), 2: ("Wein", 4, 5, 5), 3: ("Schnaps", 2, 30, 1),
                  4: ("Kaffee", 3, -3, 6)}


        dialog_menue = DialogMenue(setup)
        sound1 = pygame.mixer.Sound('../Sound/Background_1.wav')
        sound1.set_volume(0)
        channel_bg = pygame.mixer.Channel(0)
        channel_bg.play(sound1, -1)  # ist das richtig so???
        timer_clock = pygame.time.Clock()
        order_menue = OrderMenue(drinks)

        # static for all:
        self.drinks = drinks
        self.dialog_menue = dialog_menue
        self.sound_count = 0  # ???
        self.inventory_active = False
        self.text_count = 50
        self.sound1 = sound1
        self.timer_clock = timer_clock
        self.order_menue = order_menue



def draw_interactables(win, win_copy, inter):
    if inter.art == "door" or inter.art == "radio":
        inter.draw_int(win, win_copy)
    if inter.art == "clock":
        inter.draw(win)


def show_dirtyrects(win, dirtyrects):
    a = 0
    for dr in dirtyrects:
        if dr:
            win.fill((255, 255, 0), dr)
            a = a + dr[2] * dr[3]
    win_size = win.get_size()
    win_a = win_size[0] * win_size[1]
    rel = a / win_a
    print("Dirtyrects: " + str(int(rel * 10000)/100))


def travel_fun(win, setup, lvl, old_room):
    new_room = False
    if lvl[old_room].chars["guy"].travel:
        new_room = lvl[old_room].chars["guy"].travel
        lvl[old_room].chars["guy"].travel = False
    if new_room == "lvl_kitchen":
        from Scripts.Level.LVL1.LVLKitchen import LVLKitchen
        lvl[new_room] = LVLKitchen(win, setup)
        lvl[new_room].chars["guy"] = lvl[old_room].chars.pop("guy")

        return new_room
    else:
        return old_room