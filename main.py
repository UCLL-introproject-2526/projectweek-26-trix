import pygame

from maps.map_module import generatemapscreen
from main_menu.menu import load_menu
from main_menu.selection import loadselectionscreen

def ensure_screen(screen):
    # zorgt voor de fullscreen op alle schermen
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

    # defaults
    player1_char = "samurai"
    player2_char = "warrior"
    selected_map = "default"

    while running:
        screen = ensure_screen(screen)

        if state == "menu":
            result = load_menu(screen)
            if result == "play":
                state = "select"
            else:
                running = False

        elif state == "select":
            # selectie-scherm retourneert nu 4 waarden
            result, player1_char, player2_char, selected_map = loadselectionscreen(screen)
            if result == "start":
                state = "game"
            else:
                state = "menu"

        elif state == "game":
            screen = ensure_screen(screen)
            result = generatemapscreen(screen, player1_char, player2_char, selected_map)
            if result == "menu":
                state = "menu"
            elif result == "restart":
                state = "select"
            else:
                running = False

    pygame.quit()


if __name__ == "__main__":
    start_game()
