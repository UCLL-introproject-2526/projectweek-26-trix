# menu.py
import pygame
import pygame.freetype
from pygame.sprite import Sprite
import os

def load_menu():
    WHITE = (255, 255, 255)
    GREY = (225, 225, 225)
    DARK_BLUE = (149, 219, 242)
    LIGHT_BLUE = (71, 192, 232)
    TITLE_COLOR = (255, 255, 255)

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 720
    FPS = 60

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
    BACKGROUND_IMAGE = os.path.join(IMAGES_DIR, "sky_background.webp")

    def create_surface_with_text(text, font_size, text_rgb):
        font = pygame.freetype.SysFont("PixelOperator8", font_size, bold=True)
        surface, _ = font.render(text, fgcolor=text_rgb)
        return surface.convert_alpha()

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

    # shared state
    state = {"result": None, "running": True}

    def play_action():
        state["result"] = "play"
        state["running"] = False

    def quit_action():
        state["result"] = "quit"
        state["running"] = False

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Warrior Hills")
    clock = pygame.time.Clock()

    background = pygame.image.load(BACKGROUND_IMAGE).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    title = UIElement(center_position=(SCREEN_WIDTH//2, 150), text="Warrior Hills", font_size=48, text_color=TITLE_COLOR)
    play_button = UIElement(center_position=(SCREEN_WIDTH//2, 350), text="Play", font_size=48, text_color=LIGHT_BLUE, action=play_action, background=True)
    quit_button = UIElement(center_position=(SCREEN_WIDTH//2, 500), text="Quit", font_size=48, text_color=LIGHT_BLUE, action=quit_action, background=True)

    ui_elements = [title, play_button, quit_button]

    while state["running"]:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state["result"] = "quit"
                state["running"] = False

        screen.blit(background, (0, 0))

        for element in ui_elements:
            element.update(mouse_pos, mouse_pressed)
            element.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return state["result"]
