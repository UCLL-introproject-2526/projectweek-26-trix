import random
import pygame

pygame.init()

# Fullscreen display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

# Window title and icon
pygame.display.set_caption("Warrior Hills")
icon = pygame.image.load("warrior hills logo.png").convert_alpha()
pygame.display.set_icon(icon)

# Load and scale background to fullscreen
background = pygame.image.load("background.jpg").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Escape to quit fullscreen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Draw background
    screen.blit(background, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
