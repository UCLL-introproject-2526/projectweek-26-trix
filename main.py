import pygame
from maps.map_module import generate_map
from main_menu.menu import load_menu

def ensure_screen(screen):
    # Als display gequit is: opnieuw initialiseren + fullscreen opnieuw zetten
    if not pygame.display.get_init():
        pygame.display.init()

    if screen is None or not pygame.display.get_surface():
        info = pygame.display.Info()
        screen = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.FULLSCREEN | pygame.SCALED
        )
    return screen

def start_game():
    pygame.init()

    info = pygame.display.Info()
    screen = pygame.display.set_mode(
        (info.current_w, info.current_h),
        pygame.FULLSCREEN | pygame.SCALED
    )

    running = True
    state = "menu"

    while running:
        screen = ensure_screen(screen)

        if state == "menu":
            result = load_menu(screen)
            if result == "play":
                state = "game"
            else:
                running = False

        elif state == "game":
            screen = ensure_screen(screen)
            result = generate_map(screen)

            if result == "menu":
                state = "menu"
            elif result == "restart":
                state = "game"
            else:
                running = False

    pygame.quit()

if __name__ == "__main__":
    start_game()
