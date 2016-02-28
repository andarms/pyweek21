from . import bootstrap
from . import game
from .states import test, splash


def main():
    g = game.Game()
    state_dict = {
        "Splash": splash.SplashState(),
        "Test": test.TestState()
    }
    g.setup_states(state_dict, "Test")
    g.main_loop()
