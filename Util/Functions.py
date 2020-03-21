
class IncreaseI:
    def __init__(self):
        self.i = -1

    def increase(self):
        self.i += 1
        return self.i


def get_coords(x, w, _cell_size):
    cell_size = _cell_size
    coord = []

    for crd in range(0, 1 + int(w / cell_size)):  # +1 weil tür an wand
        coord.append(x + crd * cell_size)
    return coord


def get_max_coord(coord):
    if len(coord["w"]) < len(coord["h"]):
        max_coord = "h"
    else:
        max_coord = "w"
    return max_coord


def get_bg_pos(setup, size):
    win_w, win_h = setup.win_w, setup.win_h
    lvl_w, lvl_h = size
    x_pos = (win_w - lvl_w) / 2
    y_pos = (win_h - lvl_h) / 2
    return x_pos, y_pos, win_w, win_h


def get_wall_size(lvl_size, ground_pos):
    lvl_w, lvl_h = lvl_size
    ground_w, ground_h = ground_pos
    w = (lvl_w - ground_w) / 2
    h = (lvl_h - ground_h) / 2

    return w, h


def get_floor_pos(bg_pos, lvl_size, wall_w, wall_h):
    x = int(bg_pos[0] + wall_w)
    y = int(bg_pos[1] + wall_h)
    w = int(lvl_size[0] - 2*wall_w)
    h = int(lvl_size[1] - 2*wall_h)
    size = (x, y, w, h)
    return size


def Raster(win, wall_w, wall_h, floor_size, lvl_size, cell_size):
    import pygame

    win_x, win_y, win_w, win_h = floor_size

    space_h = int((win_w - 1) // cell_size)
    space_v = int((win_h - 1) // cell_size)
    wall_w = lvl_size[0] + wall_w
    wall_h = lvl_size[1] + wall_h

    font = pygame.font.SysFont('Courier', 30, True)

    # text:
    for i in range(0, space_h + 1):
        for j in range(0, space_v + 1):
            text = font.render(str(j) + "," + str(i), 1, (0, 0, 0))
            win.blit(text, (wall_w + i * 64, wall_h + j * 64))
    # senkrecht:
    for i in range(0, space_h + 1):
        pygame.draw.line(win, (0, 0, 0), (wall_w + i * 64, wall_h),
                         (wall_w + i * 64, win_h - wall_h))
    # waagrecht:
    for i in range(0, space_v + 1):
        pygame.draw.line(win, (0, 0, 0), (wall_w, wall_h + i * 64),
                         (win_w - wall_w, wall_h + i * 64))


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

