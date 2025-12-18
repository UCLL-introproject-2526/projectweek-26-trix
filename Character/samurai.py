import pygame
from animation import Animation
from utility import load_images

SCALE = 5.8
HBX, HBY, HBW, HBH = 32, 45, 26, 36


class Samurai:
    def __init__(self, x, y, controls):
        self.controls = controls

        self.animations = {
            "idle":   Animation(load_images("Sprites/idle"),   0.10, loop=True),
            "run":    Animation(load_images("Sprites/run"),    0.15, loop=True),
            "jump":   Animation(load_images("Sprites/jump"),   0.12, loop=True),
            "attack": Animation(load_images("Sprites/attack"), 0.20, loop=False),
        }

        self.state = "idle"
        self.facing_right = True

        self.image = self._scale_image(self.animations[self.state].get_image())
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = pygame.Rect(
            self.rect.x + int(HBX * SCALE),
            self.rect.y + int(HBY * SCALE),
            int(HBW * SCALE),
            int(HBH * SCALE)
        )

        self.attack_hitbox = None
        self.attack_done = False
        self.attack_frame = 2
        self.damage_applied = False

        self.prev_space = False
        self.prev_z = False

        self.speed = int(4 * SCALE)
        self.vel_y = 0
        self.gravity = 0.7 * SCALE
        self.jump_strength = 8 * SCALE
        self.on_ground = True
        self.ground_y = y

    def _scale_image(self, img):
        w = int(img.get_width() * SCALE)
        h = int(img.get_height() * SCALE)
        return pygame.transform.scale(img, (w, h))

    def start_attack(self):
        self.state = "attack"
        self.attack_done = False
        self.damage_applied = False
        self.animations["attack"].reset()

    def update(self, keys):
        space_now = keys[self.controls["attack"]]
        space_pressed = space_now and not self.prev_space
        self.prev_space = space_now

        z_now = keys[self.controls["jump"]]
        z_pressed = z_now and not self.prev_z
        self.prev_z = z_now

        moving = False

        if space_pressed and self.state != "attack":
            self.start_attack()

        if keys[self.controls["right"]]:
            self.rect.x += self.speed
            self.facing_right = True
            moving = True
        elif keys[self.controls["left"]]:
            self.rect.x -= self.speed
            self.facing_right = False
            moving = True

        if z_pressed and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False

        if not self.on_ground:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.vel_y = 0
                self.on_ground = True

        if self.state != "attack":
            if not self.on_ground:
                self.state = "jump"
            else:
                self.state = "run" if moving else "idle"

        anim = self.animations[self.state]
        anim.update()

        img = self._scale_image(anim.get_image())
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        if self.state == "attack":
            if int(anim.index) == self.attack_frame and not self.attack_done:
                self.create_attack_hitbox()
                self.attack_done = True
            else:
                self.attack_hitbox = None

            if anim.finished():
                self.attack_hitbox = None
                self.state = "idle"
        else:
            self.attack_hitbox = None

        self.hitbox.topleft = (
            self.rect.x + int(HBX * SCALE),
            self.rect.y + int(HBY * SCALE)
        )

    def create_attack_hitbox(self):
        sword_w = int(20 * SCALE)
        sword_h = int(45 * SCALE)
        sword_y = self.rect.y + int(30 * SCALE)

        if self.facing_right:
            self.attack_hitbox = pygame.Rect(
                self.rect.right - int(30 * SCALE),
                sword_y,
                sword_w,
                sword_h
            )
        else:
            self.attack_hitbox = pygame.Rect(
                self.rect.left - sword_w + int(30 * SCALE),
                sword_y,
                sword_w,
                sword_h
            )

    def clamp_to_screen(self, screen_width):
        margin = int(35 * SCALE)
        if self.rect.left < -margin:
            self.rect.left = -margin
        if self.rect.right > screen_width + margin:
            self.rect.right = screen_width + margin

        self.hitbox.topleft = (
            self.rect.x + int(HBX * SCALE),
            self.rect.y + int(HBY * SCALE)
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)