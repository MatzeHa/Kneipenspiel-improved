
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
 #   wall_w = wall_h
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
    def __init__(self, waiter, drinks, clock, raster, order_menue, dialog_menue, obstacles, interactables,
                 surf_text, music1, sound_count, inventory_active, text_count, sound1, radio, kerzen_list,
                 door_pos, chairs, halo_count, timer_clock, guy, guests, filter_halo):
        import pygame
        pygame.init()
        # static for all:
        self.drinks = drinks
        self.sound1 = sound1
        self.order_choose_font = pygame.font.SysFont('Courier', 33, True)
        self.order_choose_font.set_underline(True)



        # static in lvl_main
        self.raster = raster
        self.music1 = music1
        self.kerzen_list = kerzen_list
        self.door_pos = door_pos

        # global vars...
        self.surf_text = surf_text
        self.dialog_menue = dialog_menue
        self.inventory_active = inventory_active
        self.text_count = text_count
        self.guy = guy

        # vars in lvl_main, always the same vars, but their values change
        self.win_copy_2 = None
        self.guests = guests
        self.waiter = waiter
        self.clock = clock
        self.order_menue = order_menue
        self.obstacles = obstacles
        self.interactables = interactables
        self.radio = radio
        self.chairs = chairs
        self.sound_count = sound_count # ???
        self.halo_count = halo_count
        self.filter_halo = filter_halo
        self.timer_clock = timer_clock

