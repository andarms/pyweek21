import math

import pygame as pg

WHITE = (255, 255, 255)
EEE = (238, 238, 238)
EE0 = (238, 238, 000)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

CONTROLS = {
    pg.K_UP:  "UP",
    pg.K_DOWN: "DOWN",
    pg.K_LEFT:  "LEFT",
    pg.K_RIGHT: "RIGHT"
}
DIR_VECTORS = {
    "UP":  (0, -1),
    "DOWN":  (0, 1),
    "LEFT":  (-1, 0),
    "RIGHT":  (1, 0)
}
DIRECTIONS = ("UP", "DOWN", "LEFT", "RIGHT")
reverse_dirs = ("RIGHT", "LEFT", "DOWN", "UP")


def get_tile(pos):
    x = math.floor(pos[0] / 32)
    y = math.floor(pos[1] / 32)
    return x, y
