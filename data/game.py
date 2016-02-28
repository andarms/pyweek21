import pygame as pg

import bootstrap


class Game():

    """CLass to control the game and the game_states"""

    def __init__(self):
        self.caption = bootstrap.CAPTION
        self.screen = pg.display.get_surface()
        self.screen_size = bootstrap.SCREEN_SIZE
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.show_fps = True
        self.done = False
        self.keys = pg.key.get_pressed()

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)

    def update(self, dt):
        if self.show_fps:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

        # if self.state.quit:
        #     self.done = True

    def draw(self):
        self.screen.fill((255, 255, 207))
        pg.display.flip()

    def main_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000
            self.event_loop()
            self.update(delta_time)
            self.draw()
