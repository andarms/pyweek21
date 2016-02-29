import pygame as pg

from . import bootstrap
from . import pathfinding
from . import util


class Map():

    def __init__(self, map_source):
        self.map_source = map_source
        self.walls_sprites = pg.sprite.Group()
        self.grid = pathfinding.GridWithWeights(
            bootstrap.GRID_SIZE[0], bootstrap.GRID_SIZE[1])
        self.grid.walls = []
        x, y = 0, 0

        for row in self.map_source:
            for col in row:
                if col == '#':
                    w = MapWall(x, y)
                    self.walls_sprites.add(w)
                    self.grid.walls.append(util.get_tile((x, y)))
                x += bootstrap.TILE_SIZE
            y += bootstrap.TILE_SIZE
            x = 0

    def draw(self, surface):
        self.walls_sprites.draw(surface)


class MapWall(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([32, 32])
        self.image.fill(util.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
