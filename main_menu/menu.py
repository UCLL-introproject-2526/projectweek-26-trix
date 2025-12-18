import pygame
import pygame.freetype
from pygame.sprite import Sprite
import os


def load_menu(screen):
    # ---------------- COLORS ----------------
    WHITE = (255, 255, 255)
    GREY = (225, 225, 225)
    DARK_BLUE = (149, 219, 242)
    LIGHT_BLUE = (71, 192, 232)
    TITLE_COLOR = (255, 255, 255)

    FPS = 60

    # ✅ gebruik het fullscreen screen dat je al hebt
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    # ---------------- PATHS ----------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.dirname(BASE_DIR)  # project root
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
    MUSIC_DIR = os.path.join(PROJECT_DIR, "music")

    # ⚠️ kies de juiste extensie die jij echt hebt
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # main_menu/
    PROJECT_DIR = os.path.dirname(BASE_DIR)                 # project root

    IMAGES_DIR = os.path.join(PROJECT_DIR, "assets", "images")
    BACKGROUND_IMAGE = os.path.join(IMAGES_DIR, "sky_background.jpg")
    MENU_MUSIC = os.path.join(MUSIC_DIR, "time_for_adventure.mp3")

    # TEXT HELPER 
    def create_surface_with_text(text, font_size, text_rgb):
        font = pygame.freetype.SysFont("PixelOperator8", font_size, bold=True)
        surface, _ = font.render(text, fgcolor=text_rgb)
        return surface.convert_alpha()

    # UI ELEMENT
    class UIElement(Sprite):
        def __init__(self, center_position, text, font_size, text_color, action=None, background=False):
            super().__init__()
            self.text_image = create_surface_with_text(text, font_size, text_color)
            self.rect = self.text_image.get_rect(center=center_position)
            self.action = action
            self.background = background
            self.hovered = False

            if self.background:
                self.box_padding_x = 250
                self.box_padding_y = 30
                self.box_rect = self.rect.inflate(self.box_padding_x, self.box_padding_y)

        def update(self, mouse_pos, mouse_pressed):
            if self.background:
                self.hovered = self.box_rect.collidepoint(mouse_pos)
                if self.hovered and mouse_pressed[0] and self.action:
                    self.action()

        def draw(self, surface):
            if self.background:
                bg_color = GREY if self.hovered else WHITE
                pygame.draw.rect(surface, bg_color, self.box_rect)
                pygame.draw.rect(surface, DARK_BLUE, self.box_rect, width=3)
            surface.blit(self.text_image, self.rect)

    # ---------------- BUTTON ACTIONS ----------------
    def stop_music():
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except Exception:
            pass

    # ---------------- INIT (GEEN pygame.init, GEEN set_mode) ----------------
    pygame.display.set_caption("Warrior Hills")
    clock = pygame.time.Clock()

    # mixer init mag, maar niet verplicht
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception as e:
        print("Menu: mixer init faalde:", e)

    # ---------------- MUSIC ----------------
    try:
        music_file = None
        if os.path.isdir(MUSIC_DIR):
            if os.path.exists(MENU_MUSIC):
                music_file = MENU_MUSIC
            else:
                candidates = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith((".mp3", ".ogg", ".wav"))]
                if candidates:
                    music_file = os.path.join(MUSIC_DIR, candidates[0])

        if music_file and pygame.mixer.get_init():
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            print(f"Menu: geen muziekbestand gevonden / mixer niet init in {MUSIC_DIR}")
    except Exception as e:
        print("Menu: kan muziek niet laden/afspelen:", e)

    # ---------------- BACKGROUND ----------------
    try:
        background = pygame.image.load(BACKGROUND_IMAGE).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print("Menu: background load faalde:", BACKGROUND_IMAGE, e)
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((0, 0, 0))

    # ---------------- UI ELEMENTS ----------------
    result = None
    running = True

    def play_action():
        nonlocal result, running
        stop_music()
        result = "play"
        running = False

    def quit_action():
        nonlocal result, running
        stop_music()
        result = "quit"
        running = False

    title = UIElement(
        center_position=(SCREEN_WIDTH // 2, 150),
        text="Warrior Hills",
        font_size=48,
        text_color=TITLE_COLOR
    )

    play_button = UIElement(
        center_position=(SCREEN_WIDTH // 2, 350),
        text="Play",
        font_size=48,
        text_color=LIGHT_BLUE,
        action=play_action,
        background=True
    )

    quit_button = UIElement(
        center_position=(SCREEN_WIDTH // 2, 500),
        text="Quit",
        font_size=48,
        text_color=LIGHT_BLUE,
        action=quit_action,
        background=True
    )

    ui_elements = [title, play_button, quit_button]

    # ---------------- MAIN LOOP ----------------
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                return "quit"

        screen.blit(background, (0, 0))

        for element in ui_elements:
            element.update(mouse_pos, mouse_pressed)
            element.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    return result
