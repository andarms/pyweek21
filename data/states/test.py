import pygame as g
from .. import bootstrap
from ..game import GameState
from ..world_map import Map


class TestState(GameState):

    """Test state to work with the map"""

    def __init__(self):
        super(TestState, self).__init__()
        self.map = Map(bootstrap.MAP_SOURCE)

    def draw(self, surface):
        surface.fill((23, 45, 56))
        self.map.draw(surface)
