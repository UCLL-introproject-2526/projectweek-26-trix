from maps.map_module import generate_map
from main_menu.menu import load_menu

def start_game():
    running = True
    state = "menu"

    while running:
        if state == "menu":
            result = load_menu()      # "play" of "quit"

            if result == "play":
                state = "game"
            else:
                running = False

        elif state == "game":
            result = generate_map()   # bv. "quit" of "menu"
            if result == "menu":
                state = "menu"
            else:
                running = False

if __name__ == "__main__":
    start_game()
