import pygame
import os
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
    
    # Music setup
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.dirname(BASE_DIR)
    MUSIC_DIR = os.path.join(PROJECT_DIR, "music")
    GAME_MUSIC = os.path.join(MUSIC_DIR, "Dragon_Castle.mp3")

    # initialize audio mixer
    try:
        pygame.mixer.init()
    except Exception as e:
        print("Warning: pygame.mixer.init() failed:", e)

    # select a music file (prefer GAME_MUSIC, else first available)
    music_file = None
    if os.path.isdir(MUSIC_DIR):
        if os.path.exists(GAME_MUSIC):
            music_file = GAME_MUSIC
        else:
            candidates = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith((".mp3", ".ogg", ".wav"))]
            if candidates:
                music_file = os.path.join(MUSIC_DIR, candidates[0])

    if music_file:
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Could not load/play music:", e)
    else:
        print(f"No music file found in {MUSIC_DIR}")


    clock = pygame.time.Clock()

    # MAAK JE SPELERS AAN
    samurai = Samurai(500, 420)     # Q/D/Z/SPACE
    warrior = Warrior(100, 385)     # ARROWS + ENTER

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
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


    pygame.mixer.music.stop()
    pygame.quit()
