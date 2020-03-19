from Scripts.Util.Functions import get_max_coord
from Scripts.Util.Functions import Raster


class Level:
    def __init__(self, win, setup, images, obst_images, wall_w, wall_h):
        self.sv = {"images": images,
                   "obst_images": obst_images,
                   "wall_w": wall_w,
                   "wall_h": wall_h,
                   "cell_size": setup.cell_size,
                   "coord": setup.coord,
                   "max_coord": get_max_coord(setup.coord),
                   "raster": Raster(win, setup.wall_w, setup.wall_h, setup.cell_size)
                   }
        self.win_copy = win.copy()
        self.win_copy_change_mode = win.copy()
