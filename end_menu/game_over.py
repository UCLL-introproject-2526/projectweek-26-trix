import pygame
import sys
import os

def game_over(screen):
    window_width, window_height = screen.get_size()
    pygame.display.set_caption("Game Over")

    black = (0, 0, 0)
    white = (255, 255, 255)
    dark_blue = (149, 219, 242)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.dirname(BASE_DIR)
    IMAGE_PATH = os.path.join(PROJECT_DIR, "assets", "images", "sky_background.jpg")

    try:
        background_image = pygame.image.load(IMAGE_PATH).convert()
        background_image = pygame.transform.scale(background_image, (window_width, window_height))
    except Exception as e:
        print(f"Warning: kon achtergrond niet laden {IMAGE_PATH}:", e)
        background_image = pygame.Surface((window_width, window_height))
        background_image.fill(black)

    my_font = pygame.font.SysFont("PixelOperator8", 90)
    game_over_surface = my_font.render("GAME OVER", False, white)
    game_over_rect = game_over_surface.get_rect(midtop=(window_width // 2, window_height // 4))

    info_font = pygame.font.SysFont("PixelOperator8", 40)
    restart_surface = info_font.render("Press R to Restart", False, white)
    restart_rect = restart_surface.get_rect(midtop=(window_width // 2, window_height // 2))

    quit_surface = info_font.render("Press Q to Quit", False, white)
    quit_rect = quit_surface.get_rect(midtop=(window_width // 2, window_height // 2 + 60))

    padding_x = 25
    padding_y = 15

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
        screen.blit(game_over_surface, game_over_rect)

        pygame.draw.rect(screen, white,
                         (restart_rect.x - padding_x, restart_rect.y - padding_y,
                          restart_rect.width + 2 * padding_x, restart_rect.height + 2 * padding_y), 2)
        pygame.draw.rect(screen, white,
                         (quit_rect.x - padding_x, quit_rect.y - padding_y,
                          quit_rect.width + 2 * padding_x, quit_rect.height + 2 * padding_y), 2)

        screen.blit(restart_surface, restart_rect)
        screen.blit(quit_surface, quit_rect)

        pygame.display.flip()
        clock.tick(60)
