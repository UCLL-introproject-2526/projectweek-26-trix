import pygame
import pygame.freetype
import os

# Kleuren en settings (zelfde stijl als menu.py)
WHITE      = (255, 255, 255)
GREY       = (225, 225, 225)
DARKBLUE   = (149, 219, 242)
LIGHTBLUE  = (71, 192, 232)
TITLECOLOR = (255, 255, 255)
FPS        = 60


def create_surface_with_text(text, fontsize, text_rgb):
    font = pygame.freetype.SysFont("PixelOperator8", fontsize, bold=True)
    surface, _ = font.render(text, fgcolor=text_rgb)
    return surface.convert_alpha()


class UIElement(pygame.sprite.Sprite):
    def __init__(self, center_position, text, fontsize, textcolor,
                 action=None, background=False):
        super().__init__()
        self.text_image = create_surface_with_text(text, fontsize, textcolor)
        self.rect = self.text_image.get_rect(center=center_position)
        self.action = action
        self.background = background
        self.hovered = False

        if self.background:
            self.box_padding_x = 250
            self.box_padding_y = 30
            self.box_rect = self.rect.inflate(self.box_padding_x,
                                              self.box_padding_y)

    def update(self, mouse_pos, mouse_pressed):
        if self.background:
            self.hovered = self.box_rect.collidepoint(mouse_pos)
            if self.hovered and mouse_pressed[0] and self.action:
                self.action()

    def draw(self, surface):
        if self.background:
            bgcolor = GREY if self.hovered else WHITE
            pygame.draw.rect(surface, bgcolor, self.box_rect)
            pygame.draw.rect(surface, DARKBLUE, self.box_rect, width=3)
        surface.blit(self.text_image, self.rect)


def loadselectionscreen(screen):
    """
    Tussenscherm:
    - Player 1 kiest karakter (samurai / warrior)
    - Player 2 kiest karakter (samurai / warrior)
    - Speler kiest map (default / map1 / map2)

    Returnt: (result, player1_char, player2_char, selected_map)
    result: "start" of "back"
    """
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()

    result = None
    running = True

    player1_char = "samurai"
    player2_char = "warrior"
    selected_map = "default"

    # ---- MAP PREVIEW IMAGES LADEN ----
    # project root = map boven main_menu
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bg1_path = os.path.join(project_dir, "background1.jpg")
    bg2_path = os.path.join(project_dir, "background2.jpg")

    preview1 = None
    preview2 = None

    try:
        if os.path.exists(bg1_path):
            preview1 = pygame.image.load(bg1_path).convert()
            preview1 = pygame.transform.scale(preview1, (250, 100))
        if os.path.exists(bg2_path):
            preview2 = pygame.image.load(bg2_path).convert()
            preview2 = pygame.transform.scale(preview2, (250, 100))
    except Exception as e:
        print("Kon map previews niet laden:", e)
    # ----------------------------------

    # Actions
    def p1_samurai():
        nonlocal player1_char
        player1_char = "samurai"

    def p1_warrior():
        nonlocal player1_char
        player1_char = "warrior"

    def p2_samurai():
        nonlocal player2_char
        player2_char = "samurai"

    def p2_warrior():
        nonlocal player2_char
        player2_char = "warrior"

    def choose_map_default():
        nonlocal selected_map
        selected_map = "default"

    def choose_map1():
        nonlocal selected_map
        selected_map = "map1"

    def choose_map2():
        nonlocal selected_map
        selected_map = "map2"

    def start_action():
        nonlocal result, running
        result = "start"
        running = False

    def back_action():
        nonlocal result, running
        result = "back"
        running = False

    # UI elementen
    title = UIElement(
        center_position=(screen_width // 2, 80),
        text="Kies characters en map",
        fontsize=48,
        textcolor=TITLECOLOR
    )

    p1_label = UIElement(
        center_position=(screen_width // 4, 150),
        text="Player 1",
        fontsize=32,
        textcolor=TITLECOLOR
    )

    p2_label = UIElement(
        center_position=(3 * screen_width // 4, 150),
        text="Player 2",
        fontsize=32,
        textcolor=TITLECOLOR
    )

    p1_samurai_button = UIElement(
        center_position=(screen_width // 4, 220),
        text="Samurai",
        fontsize=32,
        textcolor=LIGHTBLUE,
        action=p1_samurai,
        background=True
    )
    p1_warrior_button = UIElement(
        center_position=(screen_width // 4, 290),
        text="Warrior",
        fontsize=32,
        textcolor=LIGHTBLUE,
        action=p1_warrior,
        background=True
    )

    p2_samurai_button = UIElement(
        center_position=(3 * screen_width // 4, 220),
        text="Samurai",
        fontsize=32,
        textcolor=LIGHTBLUE,
        action=p2_samurai,
        background=True
    )
    p2_warrior_button = UIElement(
        center_position=(3 * screen_width // 4, 290),
        text="Warrior",
        fontsize=32,
        textcolor=LIGHTBLUE,
        action=p2_warrior,
        background=True
    )

    map_default_button = UIElement(
        center_position=(screen_width // 2, 380),
        text="Standaard map",
        fontsize=30,
        textcolor=LIGHTBLUE,
        action=choose_map_default,
        background=True
    )

    map1_button = UIElement(
        center_position=(screen_width // 2, 440),
        text="Map 1",
        fontsize=30,
        textcolor=LIGHTBLUE,
        action=choose_map1,
        background=True
    )

    map2_button = UIElement(
        center_position=(screen_width // 2, 520),
        text="Map 2",
        fontsize=30,
        textcolor=LIGHTBLUE,
        action=choose_map2,
        background=True
    )

    start_button = UIElement(
        center_position=(screen_width // 2, 620),
        text="Start",
        fontsize=40,
        textcolor=LIGHTBLUE,
        action=start_action,
        background=True
    )

    back_button = UIElement(
        center_position=(screen_width // 2, 690),
        text="Terug",
        fontsize=28,
        textcolor=LIGHTBLUE,
        action=back_action,
        background=True
    )

    elements = [
        title,
        p1_label, p2_label,
        p1_samurai_button, p1_warrior_button,
        p2_samurai_button, p2_warrior_button,
        map_default_button, map1_button, map2_button,
        start_button, back_button,
    ]

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back", player1_char, player2_char, selected_map
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back", player1_char, player2_char, selected_map

        screen.fill((0, 0, 0))

        for e in elements:
            e.update(mouse_pos, mouse_pressed)
            e.draw(screen)

        # kleine previews naast de map-knoppen
        # bij Map 1
        if preview1:
            screen.blit(preview1, (screen_width // 2 - 130, 460))
        # bij Map 2
        if preview2:
            screen.blit(preview2, (screen_width // 2 - 130, 540))

        pygame.display.flip()
        clock.tick(FPS)

    return result, player1_char, player2_char, selected_map
