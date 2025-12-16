import pygame
from Character.samurai import Samurai
from Character.warrior import Warrior

def generate_map():

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(background, (0, 0))
        pygame.display.update()
        clock.tick(60)

    samurai = Samurai (500, 310)     # Q/D/Z/SPACE
    warrior = Warrior(100, 330)     # ARROWS + ENTER

    running = True
    while running:
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