import pygame
import os
from animation import Animation
from utility import load_images

# scale (vergrooting van mannetje zal alles veranderen)
SCALE = 5.8

# originele hitbox (voor 96x96 sprite)
HBX, HBY, HBW, HBH = 32, 25, 32, 55


class Samurai:
    def __init__(self, x, y):
        self.animations = {
            "idle":   Animation(load_images("Sprites/idle"),   0.10, loop=True),
            "run":    Animation(load_images("Sprites/run"),    0.15, loop=True),
            "jump":   Animation(load_images("Sprites/jump"),   0.12, loop=True),
            "attack": Animation(load_images("Sprites/attack"), 0.20, loop=False),
        }

        self.state = "idle"
        self.facing_right = True

        # image & rect
        self.image = self.animations[self.state].get_image()
        self.image = self._scale_image(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))

        # hitbox
        self.hitbox = pygame.Rect(
            self.rect.x + int(HBX * SCALE),
            self.rect.y + int(HBY * SCALE),
            int(HBW * SCALE),
            int(HBH * SCALE)
        )

        # attack
        self.attack_hitbox = None
        self.attack_done = False
        self.attack_frame = 2

        # ✅ health + damage control
        self.max_hp = 100
        self.hp = 100
        self.damage_applied = False  # voorkomt meerdere hits per attack

        # input edge detection
        self.prev_space = False
        self.prev_z = False

        # movement
        self.speed = int(4 * SCALE)
        self.vel_y = 0
        self.gravity = 0.7 * SCALE
        self.jump_strength = 8 * SCALE
        self.on_ground = True
        self.ground_y = y

        # health
        self.max_hp = 100
        self.hp = 100
        self.dead_called = False

        # load healthbar images
        self.healthbar_images = {}
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(base_dir)
            images_dir = os.path.join(project_dir, "healthbar")
            for val in range(100, -10, -10):
                fname = os.path.join(images_dir, f"healthbar_{val}.png")
                if os.path.exists(fname):
                    img = pygame.image.load(fname).convert_alpha()
                    self.healthbar_images[val] = img
        except Exception:
            self.healthbar_images = {}

    def _scale_image(self, img):
        w = int(img.get_width() * SCALE)
        h = int(img.get_height() * SCALE)
        return pygame.transform.scale(img, (w, h))

    # ✅ damage function
    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        # call game over when hp reaches 0 (once)
        if self.hp == 0 and not self.dead_called:
            self.dead_called = True
            try:
                from end_menu.game_over import game_over
                game_over()
            except Exception as e:
                print("game_over call failed:", e)

    def start_attack(self):
        self.state = "attack"
        self.attack_done = False
        self.damage_applied = False  # ✅ reset per attack
        self.animations["attack"].reset()

    def update(self, keys):
        # key press detection
        space_now = keys[pygame.K_SPACE]
        space_pressed = space_now and not self.prev_space
        self.prev_space = space_now

        z_now = keys[pygame.K_z]
        z_pressed = z_now and not self.prev_z
        self.prev_z = z_now

        moving = False

        # start attack
        if space_pressed and self.state != "attack":
            self.start_attack()

        # movement & jump (not during attack)
        if self.state != "attack":
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                self.facing_right = True
                moving = True
            elif keys[pygame.K_q]:
                self.rect.x -= self.speed
                self.facing_right = False
                moving = True

            if z_pressed and self.on_ground:
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

        # state
        if self.state != "attack":
            if not self.on_ground:
                self.state = "jump"
            else:
                self.state = "run" if moving else "idle"

        # animation
        anim = self.animations[self.state]
        anim.update()

        img = anim.get_image()
        img = self._scale_image(img)

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        # attack hitbox + finish
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

        # update player hitbox
        self.hitbox.topleft = (
            self.rect.x + int(HBX * SCALE),
            self.rect.y + int(HBY * SCALE)
        )

    # ATTACK HITBOX
    def create_attack_hitbox(self):
        sword_w = int(35 * SCALE)
        sword_h = int(55 * SCALE)
        sword_y = self.rect.y + int(32 * SCALE)

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

    # clamp zodat hij niet uit scherm loopt
    def clamp_to_screen(self, screen_width):
        margin = int(35 * SCALE)

        if self.rect.left < -margin:
            self.rect.left = -margin

        if self.rect.right > screen_width + margin:
            self.rect.right = screen_width + margin

        # hitbox mee corrigeren
        self.hitbox.topleft = (
            self.rect.x + int(HBX * SCALE),
            self.rect.y + int(HBY * SCALE)
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # draw healthbar fixed top-right
        top_margin = 20
        right_margin = 20
        screen_w = screen.get_width()
        if self.healthbar_images:
            step = (self.hp // 10) * 10
            step = max(0, min(100, step))
            hb_img = self.healthbar_images.get(step)
            if hb_img:
                x = screen_w - hb_img.get_width() - right_margin
                screen.blit(hb_img, (x, top_margin))
        else:
            hp_ratio = self.hp / self.max_hp
            bar_w = 150
            bar_h = 16
            x = screen_w - bar_w - right_margin
            pygame.draw.rect(screen, (255,0,0), (x, top_margin, bar_w, bar_h))
            pygame.draw.rect(screen, (0,255,0), (x, top_margin, int(bar_w * hp_ratio), bar_h))
