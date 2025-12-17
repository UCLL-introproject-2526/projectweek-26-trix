import pygame
from animation import Animation
from utility import load_images

SCALE = 5.0  # pas aan als je warrior groter/kleiner wil

# hitbox (basiswaarden, schalen mee)
BASE_HBX, BASE_HBY, BASE_HBW, BASE_HBH = 54, 47, 54, 60

# sword/attack hitbox (basiswaarden, schalen mee)
BASE_SWORD_X = 53
BASE_SWORD_Y = 45
BASE_SWORD_W = 50
BASE_SWORD_H = 70


class Warrior:
    def __init__(self, x, y):
        self.animations = {
            "idle":   Animation(load_images("Sprites1/warrior/idle"),   0.10, loop=True),
            "run":    Animation(load_images("Sprites1/warrior/run"),    0.15, loop=True),
            "jump":   Animation(load_images("Sprites1/warrior/jump"),   0.12, loop=True),
            "attack": Animation(load_images("Sprites1/warrior/attack"), 0.20, loop=False),
            "hurt":   Animation(load_images("Sprites1/warrior/hurt"),   0.15, loop=False),
        }

        self.state = "idle"
        self.facing_right = True

        self.image = self._scale_image(self.animations[self.state].get_image())
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = pygame.Rect(
            self.rect.x + int(BASE_HBX * SCALE),
            self.rect.y + int(BASE_HBY * SCALE),
            int(BASE_HBW * SCALE),
            int(BASE_HBH * SCALE),
        )

        # attack
        self.attack_hitbox = None
        self.attack_done = False
        self.attack_frame = 2

        # key edge detection (zodat attack niet hapert)
        self.prev_attack = False
        self.prev_jump = False

        # movement / jump physics
        self.speed = int(4 * SCALE)
        self.vel_y = 0
        self.gravity = 0.7 * SCALE
        self.jump_strength = 10 * SCALE
        self.on_ground = True
        self.ground_y = y

    def _scale_image(self, img):
        w = int(img.get_width() * SCALE)
        h = int(img.get_height() * SCALE)
        return pygame.transform.scale(img, (w, h))

    def start_attack(self):
        self.state = "attack"
        self.attack_done = False
        self.attack_hitbox = None
        self.animations["attack"].reset()

    def update(self, keys):
        # --- Arrow controls ---
        left_now = keys[pygame.K_LEFT]
        right_now = keys[pygame.K_RIGHT]

        jump_now = keys[pygame.K_UP]
        jump_pressed = jump_now and not self.prev_jump
        self.prev_jump = jump_now

        # ✅ ENTER en NUMPAD ENTER
        attack_now = keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]
        attack_pressed = attack_now and not self.prev_attack
        self.prev_attack = attack_now

        moving = False

        # start attack 1x
        if attack_pressed and self.state != "attack":
            self.start_attack()

        # movement & jump alleen als je niet attackt
        if self.state != "attack":
            if right_now:
                self.rect.x += self.speed
                self.facing_right = True
                moving = True
            elif left_now:
                self.rect.x -= self.speed
                self.facing_right = False
                moving = True

            if jump_pressed and self.on_ground:
                self.vel_y = -self.jump_strength
                self.on_ground = False

        # gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.vel_y = 0
                self.on_ground = True

        # state selection (if not attacking)
        if self.state != "attack":
            if not self.on_ground:
                self.state = "jump"
            else:
                self.state = "run" if moving else "idle"

        # update animation
        anim = self.animations[self.state]
        anim.update()

        img = self._scale_image(anim.get_image())
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        # attack hitbox timing + finish
        if self.state == "attack":
            if int(anim.index) == self.attack_frame and not self.attack_done:
                self.create_attack_hitbox()
                self.attack_done = True
            else:
                self.attack_hitbox = None

            if anim.finished():
                self.attack_hitbox = None
                self.state = "jump" if not self.on_ground else ("run" if moving else "idle")
        else:
            self.attack_hitbox = None

        # update player hitbox
        self.hitbox.topleft = (
            self.rect.x + int(BASE_HBX * SCALE),
            self.rect.y + int(BASE_HBY * SCALE),
        )

    def create_attack_hitbox(self):
        sword_x = int(BASE_SWORD_X * SCALE)
        sword_y = self.rect.y + int(BASE_SWORD_Y * SCALE)
        sword_w = int(BASE_SWORD_W * SCALE)
        sword_h = int(BASE_SWORD_H * SCALE)

        if self.facing_right:
            self.attack_hitbox = pygame.Rect(
                self.rect.right - sword_x,
                sword_y,
                sword_w,
                sword_h
            )
        else:
            self.attack_hitbox = pygame.Rect(
                self.rect.left - sword_w + sword_x,
                sword_y,
                sword_w,
                sword_h
            )

    # ✅ NIEUW: clamp zodat hij niet uit scherm loopt
    def clamp_to_screen(self, screen_width):
        margin = int(80 * SCALE)  # hoe ver hij mag "in" het scherm lopen

        if self.rect.left < -margin:
         self.rect.left = -margin

        if self.rect.right > screen_width + margin:
            self.rect.right = screen_width + margin

    # hitbox mee corrigeren
        self.hitbox.topleft = (
        self.rect.x + int(BASE_HBX * SCALE),
        self.rect.y + int(BASE_HBY * SCALE)
    )


    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # debug (zet uit als je wil)
        # pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)
        # if self.attack_hitbox:
        #     pygame.draw.rect(screen, (255, 0, 0), self.attack_hitbox, 2)
