
from math import pi, hypot
import pygame as pg
from random import uniform

from objects.bubble import Bubble
from objects.body import Body
from gui.text_box import TextBox
from special_effects import add_effect
from data.config import SCR_H, SCR_W, SCR_H2, SCR_W2, ROOM_RADIUS
from data.colors import WHITE
from data.paths import FONT_1
from data.mobs import BOSS_SKELETON_BODY


class Room:
    """
    List of bullets is made separately from list of mobs, because
    when mob is dead and deleted, its bullets should continue existing.
    'new_mobs' is a temporary list of mobs, which is created
    to draw the mobs of room player is being transported to.
    When player is transported, self.mobs = self.new_mobs.copy().
    Text is a text text_surface of room, containing rules of the game.
    Screen rectangle is used to check if mob's rectangle collides
    with it. If yes, then a mob is drawn.
    Gravity radius is a radius of circle around player, in which bubbles
    gravitate to player.
    'Bottom effects' are drawn below player, mobs, bubbles and bullets,
    other effects are 'Top effects'.
    """
    bubbles = list()
    mobs = list()
    new_mobs = list()
    bullets = list()
    homing_bullets = list()
    bottom_effects = list()
    top_effects = list()
    text = None
    screen_rect = pg.Rect(0, 0, SCR_W, SCR_H)
    gravity_radius = 160
    boss_skeleton = Body(BOSS_SKELETON_BODY)
    boss_position_marker = 0

    def __init__(self):
        self.set_text('')
        self.boss_skeleton.update(SCR_W2, SCR_H2, 0, (0, 0), 0.5 * pi)

    def reset(self, new_game=False):
        """
        Method is called when a new game is started
        or a new room is visited_rooms. Resets all room data.
        """
        self.bubbles = []
        self.bullets = []
        self.homing_bullets = []
        self.top_effects = []
        self.bottom_effects = []
        self.mobs = [] if new_game else self.new_mobs.copy()
        self.new_mobs = []
        if new_game:
            self.boss_position_marker = 0

    def check_boss(self):
        if self.boss_position_marker in [1, 2]:
            self.boss_position_marker -= 1
        for mob in self.new_mobs:
            if mob.name in ['BossLeg', 'BossHead', 'BossHand']:
                self.boss_position_marker = 2
                break

    def set_new_mobs(self, new_mobs):
        self.new_mobs = new_mobs
        self.check_boss()

    def set_text(self, text):
        """
        :param text: list of strings
        sets background room text, explaining the rules of the game
        """
        self.text = TextBox(text, FONT_1, int(47 * SCR_H/600), True,
                            WHITE, (2/3 * SCR_H, 11/60 * SCR_H))

    def delete_needless_bullets(self):
        """
        Method removes those bullets from list, that hit a target or are outside the room,
        and reduces the length of list to 100, if it is > 100.
        So the size of list becomes limited to avoid
        the situation of infinite filling the list.
        """
        tmp_bullets = []
        for i, bullet in enumerate(self.bullets):
            if bullet.is_outside() or bullet.hit_the_target:
                tmp_bullets.append(i)

        tmp_bullets.reverse()
        for index in tmp_bullets:
            self.bullets.pop(index)

        while len(self.bullets) > 100:
            self.bullets.pop(0)

    def delete_dead_homing_bullets(self):
        """
        Method deletes homing bullets with not
        positive health from list of homing bullets.
        """
        dead_bullets = []
        for i, bullet in enumerate(self.homing_bullets):
            if bullet.health <= 0 or bullet.hit_the_target:
                dead_bullets.append(i)

        dead_bullets.reverse()
        for index in dead_bullets:
            self.homing_bullets.pop(index)

    def delete_needless_bubbles(self):
        """
        removes those bubbles from list, which are outside
        the room, so that player can't eat them
        """
        tmp_bubbles = []
        for index in range(len(self.bubbles)):
            if self.bubbles[index].is_outside():
                tmp_bubbles.append(index)
                tmp_bubbles.reverse()
        for index in tmp_bubbles:
            self.bubbles.pop(index)

    @staticmethod
    def delete_needless_effects(effects):
        """
        removes those effects from the given
        list, which have stopped running
        """
        tmp_effects = []
        for index in range(len(effects)):
            if not effects[index].running:
                tmp_effects.append(index)
        tmp_effects.reverse()
        for index in tmp_effects:
            effects.pop(index)

    def delete_dead_mobs(self):
        """
        Method deletes mobs with not positive health from
        list of mobs and replaces them with bubbles.
        """
        dead_mobs = []
        index = 0
        for mob in self.mobs:
            if mob.health <= 0:
                dead_mobs.append(index)
                self.add_bubbles(mob.x, mob.y, mob.bubbles)
            index += 1

        dead_mobs.reverse()
        for index in dead_mobs:
            self.mobs.pop(index)

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)

        self.delete_needless_bullets()

    def update_homing_bullets(self, player_x, player_y, dt):
        for bullet in self.homing_bullets:
            bullet.update(dt, player_x, player_y)

        self.delete_dead_homing_bullets()

    def update_bubbles(self, x, y, dt):
        for bubble in self.bubbles:
            bubble.update(x, y, dt)

        self.delete_needless_bubbles()

    def update_effects(self, dt):
        for effect in self.top_effects:
            effect.update(dt)
        for effect in self.bottom_effects:
            effect.update(dt)

        self.delete_needless_effects(self.top_effects)
        self.delete_needless_effects(self.bottom_effects)

    def handle_bullet_explosion(self, x, y):
        """
        Changes mobs' states according to their positions relative
        to the explosion, and adds appropriate effects.
        :param x: x-coord of bullet
        :param y: y-coord of bullet

        """
        for mob in self.mobs:
            if hypot(x - mob.x, y - mob.y) <= 200:
                mob.health -= 20
                mob.change_body()
                add_effect('BigHitLines', self.top_effects, mob.x, mob.y)
        add_effect('PowerfulExplosion', self.bottom_effects, x, y)
        add_effect('Flash', self.top_effects)

    def move_objects(self, offset):
        """
        Method is called when the player is being transported
        to the next room. The objects of previous room become
        moved by the given offset to be drawn properly during
        player's transportation
        """
        for bubble in self.bubbles:
            bubble.move(*offset)

        for mob in self.mobs:
            mob.move(*offset)

        for bullet in self.bullets:
            bullet.move(*offset)

        for bullet in self.homing_bullets:
            bullet.move(*offset)

        self.boss_skeleton.update(SCR_W2, SCR_H2, 0, (0, 0), 0.5 * pi)
        if self.boss_position_marker == 1:
            self.boss_skeleton.move(*offset)

    def set_gravity_radius(self, gravity_radius):
        """
        Sets the new radius of player's gravitational field
        :param gravity_radius: radius of circle, in which
               the player's gravity exists
        """
        if self.mobs:
            self.gravity_radius = gravity_radius

            for bubble in self.bubbles:
                bubble.gravity_r = gravity_radius

    def maximize_gravity(self):
        """
        Method is called when all mobs in the room are dead.
        The radius of player's gravitational field is set equal to
        the diameter of room, so that every bubble starts
        gravitating to player regardless of his position in the room.
        Also speeds of bubbles are maximized to reach player faster.
        """

        for bubble in self.bubbles:
            bubble.gravity_r = 2 * ROOM_RADIUS
            bubble.maximize_vel()

    def update_mobs(self, player_x, player_y, dt):
        generated_mobs = list()
        target = [player_x, player_y]
        for mob in self.mobs:
            mob.update(target, self.bullets, self.homing_bullets,
                       generated_mobs, self.screen_rect, dt)

        self.mobs.extend(generated_mobs)
        self.delete_dead_mobs()

    def update_new_mobs(self, player_x, player_y, dt):
        """
        Method updates positions and bodies of mobs of the room,
        player is being transported to.
        """
        target = (player_x, player_y)
        for mob in self.new_mobs:
            mob.update_pos(dt)
            mob.gamma = mob.count_gamma()
            if mob.body_rect.colliderect(self.screen_rect):
                mob.update_body(dt, target)

    def set_screen_rect(self, pos):
        self.screen_rect.center = pos

    def game_is_over(self):
        return self.boss_position_marker == 2 and not self.mobs

    def update(self, player_pos, dt):
        self.set_screen_rect(player_pos)

        self.update_mobs(*player_pos, dt)
        self.update_bubbles(*player_pos, dt)
        self.update_bullets(dt)
        self.update_homing_bullets(*player_pos, dt)
        self.update_effects(dt)

        if not self.mobs:
            self.maximize_gravity()

    def add_bubbles(self, mob_x, mob_y, bubbles):
        """
        :param mob_x: x coord of dead mob
        :param mob_y: y coord of dead mobs
        :param bubbles: list of the number of bubbles of 3 types: small, medium, big
        """
        for bubble_type in bubbles:
            for i in range(bubbles[bubble_type]):
                angle = uniform(0, 2 * pi)
                self.bubbles.append(Bubble(mob_x, mob_y, angle, self.gravity_radius, bubble_type))

    def draw_text(self, surface, dx, dy):
        self.text.draw(surface, dx, dy)

    def draw_bubbles(self, surface, dx, dy):
        for bubble in self.bubbles:
            bubble.draw(surface, dx, dy)

    def draw_mobs(self, surface, dx, dy):
        for mob in self.mobs:
            if mob.body_rect.colliderect(self.screen_rect):
                mob.body.draw(surface, dx, dy)

    def draw_new_mobs(self, surface, dx, dy):
        for mob in self.new_mobs:
            if mob.body_rect.colliderect(self.screen_rect):
                mob.body.draw(surface, dx, dy)

    def draw_boss_skeleton(self, surface, dx, dy):
        if self.boss_position_marker:
            self.boss_skeleton.draw(surface, dx, dy)

    def draw_bombs(self, surface, dx, dy):
        for bullet in self.bullets:
            if bullet.vel == 0:
                bullet.draw(surface, dx, dy)

    def draw_bullets(self, surface, dx, dy):
        for bullet in self.bullets:
            if bullet.vel != 0:
                bullet.draw(surface, dx, dy)

        for bullet in self.homing_bullets:
            bullet.draw(surface, dx, dy)

    def draw_top_effects(self, surface, dx, dy):
        for effect in self.top_effects:
            effect.draw(surface, dx, dy)

    def draw_bottom_effects(self, surface, dx, dy):
        for effect in self.bottom_effects:
            effect.draw(surface, dx, dy)