import math
import random
import itertools

import pygame as pg

from . import pathfinding, util


def hit_rect_collide(left, right):
    return left.hit_rect.colliderect(right.rect)


class Actor(pg.sprite.Sprite):

    """docstring for Actor"""

    def __init__(self, pos, spritesheet, size, *groups):
        super(Actor, self).__init__(*groups)
        self.speed = 250  # px/seg
        self.direction = "DOWN"
        self.old_direction = None
        self.direction_stack = []
        self.hp = 100
        self.collide = False
        self.size = size
        self.dirty = 1
        self.image = pg.Surface([32, 32])
        self.image.fill((155, 55, 23))
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_rect = self.rect.copy()
        self.hit_rect.midbottom = self.rect.midbottom

    def get_frames(self, spritesheet):
        """ Must be overloaded in child objects"""
        pass

    def make_frame_dict(self, frames):
        """ Must be overloaded in child objects"""
        pass

    def add_direction(self, direction):
        """
        Add direction to the sprite's direction stack and change current
        direction.
        """
        if direction in self.direction_stack:
            self.direction_stack.remove(direction)
        self.direction_stack.append(direction)
        self.direction = direction

    def pop_direction(self, direction):
        """
        Remove direction from direction stack and change current direction
        to the top of the stack (if not empty).
        """
        if direction in self.direction_stack:
            self.direction_stack.remove(direction)
        if self.direction_stack:
            self.direction = self.direction_stack[-1]

    def update(self, dt, now, walls):
        # self.animate(now)
        if self.hp <= 0:
            self.kill()
        if self.direction_stack:
            direction_vector = util.DIR_VECTORS[self.direction]
            self.rect.x += direction_vector[0] * self.speed * dt
            self.rect.y += direction_vector[1] * self.speed * dt
            self.hit_rect.center = self.rect.center
        self.check_collitions(walls)

    def animate(self, now=0):
        if self.direction != self.old_direction:
            self.walkframes = self.frames[self.direction]
            self.old_direction = self.direction
            self.dirty = 1
        if self.dirty or now-self.animate_timer > 1000/self.animate_fps:
            if self.direction_stack:
                self.image = next(self.walkframes)
                self.animate_timer = now
                self.dirty = 0
            else:
                self.image = self.idelframes[self.direction]

    def check_collitions(self, walls):
        wall = pg.sprite.spritecollideany(self, walls, hit_rect_collide)
        if wall:
            if self.direction == "LEFT":
                self.hit_rect.left = wall.rect.right
            elif self.direction == "RIGHT":
                self.hit_rect.right = wall.rect.left
            elif self.direction == "UP":
                self.hit_rect.top = wall.rect.bottom
            elif self.direction == "DOWN":
                self.hit_rect.bottom = wall.rect.top
            self.rect.center = self.hit_rect.center
            self.collide = True
        else:
            self.collide = False

    def attack(self, dt, direction=None, *groups):
        if not direction:
            direction = self.direction
        if self.cooldown > 0:
            self.cooldown -= dt
        else:
            Bullet(self.rect.center, direction, self.bullet_color,  *groups)
            self.cooldown = self.cooldowntime

    def take_damage(self, damage):
        self.hp -= damage
        self.dirty = 1
        if self.hp <= 0:
            return self.value

    def kill(self):
        super(Actor, self).kill()
        for _ in xrange(random.randint(25, 50)):
            Fragment(self.rect.center)
        if not self.exploded:
            hud.KillLabel(self.rect.topleft, self.value)
            rand = random.random()
            if rand > .66 and rand < 0.77:
                PickUp(self.rect.center)
        util.sfx.play(self.explosion_sound)
        del self


class Player(Actor):

    def __init__(self, pos, *groups):
        size = (32, 64)
        image = "player"
        super(Player, self).__init__(pos, image, size, *groups)
        self.speed = 300
        self.bullets = pg.sprite.Group()
        self.cooldowntime = 0.4
        self.score = 0
        self.value = 0

    def make_frame_dict(self, frames):
        frame_dict = {}
        for i, direct in enumerate(util.DIRECTIONS):
            self.idelframes[direct] = frames[i][0]
            frame_dict[direct] = itertools.cycle(frames[i])
        return frame_dict

    def get_frames(self, spritesheet):
        sheet = util.GFX[spritesheet]
        all_frames = util.split_sheet(sheet, self.size, 4, 4)
        return all_frames

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.add_direction(event.key)
        if event.type == pg.KEYUP:
            self.pop_direction(event.key)

    def add_direction(self, key):
        if key in util.CONTROLS:
            direction = util.CONTROLS[key]
            super(Player, self).add_direction(direction)

    def pop_direction(self, key):
        if key in util.CONTROLS:
            direction = util.CONTROLS[key]
            super(Player, self).pop_direction(direction)

    def attack(self, dt, direction, *groups):
        if not direction:
            direction = self.direction
        if self.cooldown > 0:
            self.cooldown -= dt
        else:
            Bullet(self.rect.center, direction, self.bullet_color,  *groups)
            util.bullets.play(self.attack_sound)
            self.cooldown = self.cooldowntime

    def update(self, dt, now, walls):
        super(Player, self).update(dt, now, walls)
        self.pos = util.get_tile(self.rect.center)


class Zombie(Actor):

    """docstring for Zombie"""

    def __init__(self, pos, image=None, *groups):
        size = (32, 32)
        if not image:
            image = "bug"
        super(Zombie, self).__init__(pos, image, size, *groups)
        self.image.fill((32, 213, 45))
        self.wait_range = (1500, 5000)
        self.speed = 50
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = 0.0
        self.change_direction()
        self.value = 10
        self.is_explosive = True
        self.animate_fps = 5.0
        self.max_damage = 15

    def make_frame_dict(self, frames):
        frame_dict = {}
        for i, direct in enumerate(util.DIRECTIONS):
            self.idelframes[direct] = frames[i][0]
            frame_dict[direct] = itertools.cycle(frames[i])
        return frame_dict

    def get_frames(self, spritesheet):
        sheet = util.GFX[spritesheet]
        all_frames = util.split_sheet(sheet, self.size, 3, 4)
        return all_frames

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.add_direction(event.key)
        if event.type == pg.KEYUP:
            self.pop_direction(event.key)

    def update(self, dt, now, walls, *args):
        """
        Choose a new direction if wait_time has expired or the sprite
        collide with the walls.
        """
        if now-self.wait_time > self.wait_delay:
            self.change_direction(now)
        super(Zombie, self).update(dt, now, walls)
        if self.collide:
            self.change_direction(now)

    def change_direction(self, now=0, direction=None):
        """
        Empty the stack and choose a new direction.  The sprite may also
        choose not to go idle (choosing direction=None)
        """
        self.direction_stack = []
        if not direction:
            direction = random.choice(util.DIRECTIONS+(None,))
        if direction:
            super(Zombie, self).add_direction(direction)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = now

    def distance(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[0])**2)


class HungryZombie(pg.sprite.Sprite):

    """docstring for HungryZombie"""

    def __init__(self, pos, *groups):
        super(HungryZombie, self).__init__()
        self.image = pg.Surface([32, 32])
        self.image.fill((83, 255, 23))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.pos = util.get_tile(pos)
        self.path = []

        self.speed = 150
        self.wait_range = (500, 2000)
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = 0.0

    def chase(self, now, player_pos, grid):
        self.path = []
        came_from, cost = pathfinding.a_star_search(
            grid, self.pos, player_pos)
        path = pathfinding.reconstruct_path(
            came_from, self.pos, player_pos)
        path.reverse()
        self.path = path
        self.wait_delay = random.randint(*self.wait_range)
        self.wait_time = now

    def update(self, dt, now, player, grid):
        if now-self.wait_time > self.wait_delay:
            self.chase(now, player.pos, grid)

        if self.path:
            next_pos = self.path[-1]
        else:
            next_pos = None

        if self.pos == next_pos:
            self.path.pop()

        if next_pos:
            if self.pos[0] < next_pos[0]:
                self.rect.x += self.speed * dt
                self.pos = util.get_tile(self.rect.topleft)
            elif self.pos[0] > next_pos[0]:
                self.rect.x -= self.speed * dt
                self.pos = util.get_tile(self.rect.midright)

            if self.pos[1] < next_pos[1]:
                self.rect.y += self.speed * dt
                self.pos = util.get_tile(self.rect.topleft)
            elif self.pos[1] > next_pos[1]:
                self.rect.y -= self.speed * dt
                self.pos = util.get_tile(self.rect.midbottom)
