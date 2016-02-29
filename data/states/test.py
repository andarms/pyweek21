import pygame as pg

from .. import actors, bootstrap, util
from ..game import GameState
from ..world_map import Map


class TestState(GameState):

    """Test state to work with the map"""

    def __init__(self):
        super(TestState, self).__init__()
        self.player_sprite = pg.sprite.GroupSingle()
        self.enemes = pg.sprite.Group()
        self.map = Map(bootstrap.MAP_SOURCE)
        self.night_bg = (25, 25, 56)
        self.day_bg = (225, 225, 255)
        self.day_duation = 36  # seg
        self.night_duation = 12
        self.day = True
        self.ticks = 0
        self.days = 0

        self.player = actors.Player((32, 32), self.player_sprite)
        self.hz = actors.HungryZombie((128, 128))
        self.hz.add(self.enemes)

    def handle_events(self, event):
        self.player.handle_events(event)

    def update(self, dt, current_time, keys):
        self.ticks += dt
        if self.day and self.ticks > self.day_duation:
            self.day = False
            self.ticks = 0

        if not self.day and self.ticks > self.night_duation:
            self.day = True
            self.ticks = 0
            self.days += 1
            print("Day: %s" % self.days)

        self.player.update(dt, current_time, self.map.walls_sprites)
        self.enemes.update(dt, current_time, self.player, self.map.grid)

    def draw(self, surface):
        if self.day:
            surface.fill(self.day_bg)
        else:
            surface.fill(self.night_bg)

        self.map.draw(surface)
        self.player_sprite.draw(surface)
        self.enemes.draw(surface)
