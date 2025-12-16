import pygame
from Characters.samurai import Samurai
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Samurai Game")
clock = pygame.time.Clock()

samurai = Samurai(200, 300)
enemy = Enemy(500, 300)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    samurai.update(keys)

    if samurai.attack_hitbox and samurai.attack_hitbox.colliderect(enemy.hitbox):
        enemy.take_damage()

    screen.fill((30, 30, 30))
    samurai.draw(screen)
    enemy.draw(screen)
    pygame.display.flip()

pygame.quit()
