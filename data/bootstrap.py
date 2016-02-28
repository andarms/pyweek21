import pygame as pg
import random

# Game consts
TILE_SIZE = 32
GRID_SIZE = (32, 20)
SCREEN_SIZE = (TILE_SIZE * GRID_SIZE[0], TILE_SIZE * GRID_SIZE[1])
CAPTION = "The Day Atfer Zombies"

pg.init()
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


MAP_SOURCE = []
for y in range(GRID_SIZE[1]):
    line = ""
    for x in range(GRID_SIZE[0]):
        line += random.choice("   #")
    MAP_SOURCE.append(line)
