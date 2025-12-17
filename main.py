from maps.map_module import generate_map
from main_menu.menu import load_menu
#from Character.samurai import Samurai
#from Character.warrior import Warrior

def start_game():
    result = load_menu()  # ❗ maar één keer

    if result == "play":
        generate_map()     
    else:
        print("Geen play, afsluiten...")

if __name__ == "__main__":
    start_game()
