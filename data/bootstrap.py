import random
import os

import pygame as pg

from . import util

pg.init()
SCREEN = pg.display.set_mode(util.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


# load resources
FONTS = util.load_all_fonts(os.path.join('resources', 'fonts'))
GFX = util.load_all_gfx("resources")
MAPS = util.load_all_maps(os.path.join('resources', 'maps'))
# SFX = util.load_all_music(os.path.join('resources', 'music'))
