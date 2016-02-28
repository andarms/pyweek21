import math

WHITE = (255, 255, 255)
EEE = (238, 238, 238)
EE0 = (238, 238, 000)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def get_tile(pos):
    x = math.floor(pos[0] / 32)
    y = math.floor(pos[1] / 32)
    return x, y
