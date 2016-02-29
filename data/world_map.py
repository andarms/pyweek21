import pygame as pg
from pytmx.util_pygame import load_pygame

from . import bootstrap
from . import pathfinding
from . import util


class Map():

    def __init__(self, map_source):
        self.all_sprites = pg.sprite.Group()
        self.visible_sprites = pg.sprite.Group()
        self.map_sprites = pg.sprite.Group()
        self.collition_sprites = pg.sprite.Group()

        self.map_source = load_pygame(bootstrap.MAPS[0])
        self.grid = pathfinding.GridWithWeights(
            self.map_source.width, self.map_source.height)
        w = self.map_source.width * util.TILE_SIZE
        h = self.map_source.height * util.TILE_SIZE
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()

        self.make_map()

    def make_map(self):
        layer = self.map_source.layers[0]
        for x, y, image in layer.tiles():
            tile = pg.sprite.Sprite(self.map_sprites, self.all_sprites)
            tile.image = image
            tile.rect = pg.Rect(
                x*util.TILE_SIZE, y*util.TILE_SIZE, util.TILE_SIZE, util.TILE_SIZE)
            self.image.blit(tile.image, tile.rect)

    def draw(self, surface, viewport):
        # self.all_sprites.draw(self.image)
        surface.blit(self.image, (0, 0), viewport)
