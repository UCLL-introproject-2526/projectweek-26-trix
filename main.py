from maps.map_module import generate_map
from main_menu.menu import load_menu

def start_game():
    result = load_menu()

    if result == "play":
        generate_map()
    else:
        print("Geen play, afsluiten...")

if __name__ == "__main__":
    start_game()