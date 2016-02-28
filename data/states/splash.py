import pygame as g
from ..game import GameState


class SplashState(GameState):

    """Splash scren"""

    def __init__(self):
        super(SplashState, self).__init__()

    def draw(self, surface):
        surface.fill((34, 236, 36))
