import pygame
import sys
import os

def game_over(screen):
    # GEEN pygame.init() en GEEN set_mode() hier!

    window_width, window_height = screen.get_size()
    pygame.display.set_caption("Game Over")

    black = (0, 0, 0)
    white = (255, 255, 255)
    dark_blue = (149, 219, 242)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.dirname(BASE_DIR)
    IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images", "game_over_screen.png")

    try:
        background_image = pygame.image.load(IMAGE_PATH).convert()
        background_image = pygame.transform.scale(background_image, (window_width, window_height))
    except Exception as e:
        print(f"kon achtergrond niet laden {IMAGE_PATH}:", e)
        background_image = pygame.Surface((window_width, window_height))
        background_image.fill(black)


    RESTART_SWORD_PATH = os.path.join(BASE_DIR, "assets", "images", "restart_sword.png")
    QUIT_SWORD_PATH = os.path.join(BASE_DIR, "assets", "images", "quit_sword.png")
    
    try:
        restart_surface = pygame.image.load(RESTART_SWORD_PATH).convert_alpha()
        quit_surface = pygame.image.load(QUIT_SWORD_PATH).convert_alpha()
    except Exception as e:
        print(f"kon knoppen niet laden:", e)
        return "quit"
    
    restart_rect = restart_surface.get_rect(
        midtop=(window_width // 2, window_height // 2)
    )
    
    quit_rect = quit_surface.get_rect(
        midtop=(window_width // 2, window_height // 2 + 120)
    )


    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    return "quit"

        screen.blit(background_image, (0, 0))


        screen.blit(background_image, (0, 0))
        screen.blit(restart_surface, restart_rect)
        screen.blit(quit_surface, quit_rect)

        pygame.display.flip()
        clock.tick(60)