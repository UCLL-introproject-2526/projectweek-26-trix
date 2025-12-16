import pygame
from Characters.samurai import Samurai
from Characters.warrior import Warrior

pygame.init()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Warrior Hills")
clock = pygame.time.Clock()

# Zet ze op verschillende startposities
samurai = Samurai (500, 310)     # Q/D/Z/SPACE
warrior = Warrior(100, 330)     # ARROWS + ENTER

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Update allebei
    samurai.update(keys)
    warrior.update(keys)

    # Teken allebei
    screen.fill((30, 30, 30))
    samurai.draw(screen)
    warrior.draw(screen)
    pygame.display.flip()

pygame.quit()
