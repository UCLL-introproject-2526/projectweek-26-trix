import pygame
from Character.samurai import Samurai
from Character.warrior import Warrior

def generate_map():
    pygame.init()

    # Fullscreen display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()

    pygame.display.set_caption("Warrior Hills")
    icon = pygame.image.load("warrior hills logo.png").convert_alpha()
    pygame.display.set_icon(icon)

    # Background
    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    clock = pygame.time.Clock()

    # MAAK JE SPELERS AAN
    samurai = Samurai(500, 420)     # Q/D/Z/SPACE
    warrior = Warrior(100, 385)     # ARROWS + ENTER

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()

        # UPDATE
        samurai.update(keys)
        warrior.update(keys)

        # BORDER (HIER) -> kan niet uit het scherm lopen
        samurai.clamp_to_screen(screen_width)
        warrior.clamp_to_screen(screen_width)

        # DRAW
        screen.blit(background, (0, 0))
        samurai.draw(screen)
        warrior.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
