import pygame
from animation import Animation
from utility import load_images

class Samurai:
    def __init__(self, x, y):
        self.animations = {
            "idle":   Animation(load_images("sprites/idle"),   0.10),
            "run":    Animation(load_images("sprites/run"),    0.15),
            "attack": Animation(load_images("sprites/attack"), 0.20),
            "jump":   Animation(load_images("sprites/jump"),   0.12),
        }

        self.state = "idle"
        self.image = self.animations[self.state].get_image()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = pygame.Rect(self.rect.x + 10, self.rect.y + 10, 40, 60)

        self.facing_right = True
        self.attack_hitbox = None
        self.attack_done = False
        self.attack_frame = 2

        # Jump physics
        self.ground_y = y
        self.vel_y = 0
        self.gravity = 0.7
        self.jump_strength = 12
        self.on_ground = True
        self.speed = 4

    def update(self, keys):
        moving = False

        # Attack (SPACE)
        if keys[pygame.K_SPACE]:
            if self.state != "attack":
                self.state = "attack"
                self.attack_done = False

        # Movement
        if self.state != "attack":
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                self.facing_right = True
                moving = True
            elif keys[pygame.K_q]:
                self.rect.x -= self.speed
                self.facing_right = False
                moving = True

            if keys[pygame.K_z] and self.on_ground:
                self.vel_y = -self.jump_strength
                self.on_ground = False

        # Gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y

            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.vel_y = 0
                self.on_ground = True

        # State
        if self.state != "attack":
            if not self.on_ground:
                self.state = "jump"
            else:
                self.state = "run" if moving else "idle"

        # Update animation
        anim = self.animations[self.state]
        anim.update()
        self.image = anim.get_image()

        # Flip if facing left
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        # Attack hitbox timing
        if self.state == "attack":
            if int(getattr(anim, "index", 0)) == self.attack_frame and not self.attack_done:
                self.create_attack_hitbox()
                self.attack_done = True
            else:
                self.attack_hitbox = None
        else:
            self.attack_hitbox = None

        self.hitbox.topleft = (self.rect.x + 10, self.rect.y + 10)

    def create_attack_hitbox(self):
        if self.facing_right:
            self.attack_hitbox = pygame.Rect(self.rect.right, self.rect.y + 20, 40, 30)
        else:
            self.attack_hitbox = pygame.Rect(self.rect.left - 40, self.rect.y + 20, 40, 30)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)
        if self.attack_hitbox:
            pygame.draw.rect(screen, (255, 0, 0), self.attack_hitbox, 2)
