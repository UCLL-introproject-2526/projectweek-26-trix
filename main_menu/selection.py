import pygame
import pygame.freetype
import os

# Kleuren en settings (zelfde stijl als menu.py)
WHITE      = (255, 255, 255)
GREY       = (225, 225, 225)
DARKBLUE   = (149, 219, 242)
LIGHTBLUE  = (71, 192, 232)
SELECT_GREEN = (38, 166, 91)
TITLECOLOR = (255, 255, 255)
FPS        = 60


def create_surface_with_text(text, fontsize, text_rgb):
    font = pygame.freetype.SysFont("PixelOperator8", fontsize, bold=True)
    surface, _ = font.render(text, fgcolor=text_rgb)
    return surface.convert_alpha()


class UIElement(pygame.sprite.Sprite):
    def __init__(self, center_position, text, fontsize, textcolor,
                 action=None, background=False, value=None, group=None):
        super().__init__()
        self.text_image = create_surface_with_text(text, fontsize, textcolor)
        self.rect = self.text_image.get_rect(center=center_position)
        self.action = action
        self.background = background
        self.hovered = False
        # selection metadata
        self.value = value
        self.group = group
        self.selected = False

        if self.background:
            # padding is relative to text width so boxes don't overlap
            text_w = self.text_image.get_width()
            self.box_padding_x = max(120, text_w + 60)
            self.box_padding_y = 20
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
            border_color = SELECT_GREEN if self.selected else DARKBLUE
            pygame.draw.rect(surface, border_color, self.box_rect, width=3)
            # draw selection indicator
            if self.selected:
                cx = self.box_rect.right - 18
                cy = self.box_rect.centery
                pygame.draw.circle(surface, SELECT_GREEN, (cx, cy), 8)
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

    # ---- MAP PREVIEW IMAGES LADEN UIT maps/assets ----
    base_dir = os.path.dirname(os.path.abspath(__file__))   # main_menu/
    project_dir = os.path.dirname(base_dir)                 # projectroot
    maps_dir = os.path.join(project_dir, "maps")
    assets_dir = os.path.join(maps_dir, "assets")

    bg1_path = os.path.join(assets_dir, "samurai_map.jpg")           # map1
    bg2_path = os.path.join(assets_dir, "factory-pixel-art-gif.jpg") # map2

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
    # --------------------------------------------------

    # Actions
    # character lists (label, key)
    characters = [
        ("Samurai", "samurai"),
        ("Warrior", "warrior"),
        ("Huntress", "huntress"),
        ("King", "king"),
        ("Martial I", "martial_hero"),
        ("Martial II", "martial_hero2"),
    ]

    # map from key -> display label
    label_map = {key: label for (label, key) in characters}

    # helper to create actions
    def make_set_player1(ch):
        def _set():
            nonlocal player1_char
            player1_char = ch
        return _set

    def make_set_player2(ch):
        def _set():
            nonlocal player2_char
            player2_char = ch
        return _set

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
        center_position=(screen_width // 4, 120),
        text="Player 1",
        fontsize=32,
        textcolor=TITLECOLOR
    )

    p2_label = UIElement(
        center_position=(3 * screen_width // 4, 120),
        text="Player 2",
        fontsize=32,
        textcolor=TITLECOLOR
    )

    # generate character buttons with spacing to avoid overlap
    p1_buttons = []
    p2_buttons = []
    start_y = 170
    spacing = 70
    for i, (label, key) in enumerate(characters):
        y = start_y + i * spacing
        p1_buttons.append(UIElement(
            center_position=(screen_width // 4, y),
            text=label,
            fontsize=28,
            textcolor=LIGHTBLUE,
            action=make_set_player1(key),
            value=key,
            group='p1',
            background=True
        ))
        p2_buttons.append(UIElement(
            center_position=(3 * screen_width // 4, y),
            text=label,
            fontsize=28,
            textcolor=LIGHTBLUE,
            action=make_set_player2(key),
            value=key,
            group='p2',
            background=True
        ))

    # map buttons (placed to the right/bottom area)
    map_x = screen_width // 2 + 120
    map_start_y = start_y
    map_spacing = 80

    map_default_button = UIElement(
        center_position=(map_x, map_start_y),
        text="Standaard map",
        fontsize=26,
        textcolor=LIGHTBLUE,
        action=choose_map_default,
        value='default',
        group='map',
        background=True
    )

    map1_button = UIElement(
        center_position=(map_x, map_start_y + map_spacing),
        text="Map 1",
        fontsize=26,
        textcolor=LIGHTBLUE,
        action=choose_map1,
        value='map1',
        group='map',
        background=True
    )

    map2_button = UIElement(
        center_position=(map_x, map_start_y + map_spacing * 2),
        text="Map 2",
        fontsize=26,
        textcolor=LIGHTBLUE,
        action=choose_map2,
        value='map2',
        group='map',
        background=True
    )

    start_button = UIElement(
        center_position=(screen_width // 2, screen_height - 100),
        text="Start",
        fontsize=36,
        textcolor=LIGHTBLUE,
        action=start_action,
        background=True
    )

    back_button = UIElement(
        center_position=(screen_width // 2, screen_height - 40),
        text="Terug",
        fontsize=26,
        textcolor=LIGHTBLUE,
        action=back_action,
        background=True
    )

    elements = [title, p1_label, p2_label]
    elements.extend(p1_buttons)
    elements.extend(p2_buttons)
    elements.extend([map_default_button, map1_button, map2_button, start_button, back_button])

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
            # update selection state for visual indicator
            if hasattr(e, 'group') and e.group:
                if e.group == 'p1':
                    e.selected = (e.value == player1_char)
                elif e.group == 'p2':
                    e.selected = (e.value == player2_char)
                elif e.group == 'map':
                    e.selected = (e.value == selected_map)
                else:
                    e.selected = False
            else:
                e.selected = False

            e.update(mouse_pos, mouse_pressed)
            e.draw(screen)

        # kleine previews naast de map-knoppen
        if preview1:  # bij Map 1
            screen.blit(preview1, (screen_width // 2 - 130, 460))
        if preview2:  # bij Map 2
            screen.blit(preview2, (screen_width // 2 - 130, 540))

        # toon geselecteerde characters onder de labels
        try:
            s1 = label_map.get(player1_char, player1_char)
            s2 = label_map.get(player2_char, player2_char)
            sel1_surf = create_surface_with_text(f"Geselecteerd: {s1}", 18, TITLECOLOR)
            sel2_surf = create_surface_with_text(f"Geselecteerd: {s2}", 18, TITLECOLOR)
            screen.blit(sel1_surf, (p1_label.rect.centerx - sel1_surf.get_width()//2, p1_label.rect.centery + 30))
            screen.blit(sel2_surf, (p2_label.rect.centerx - sel2_surf.get_width()//2, p2_label.rect.centery + 30))
        except Exception:
            pass

        pygame.display.flip()
        clock.tick(FPS)

    return result, player1_char, player2_char, selected_map
