import bootstrap
from . import game
from .states import splash


def main():
    g = game.Game()
    state_dict = {
        "Splash": splash.SplashState()
    }
    g.setup_states(state_dict, "Splash")
    g.main_loop()
