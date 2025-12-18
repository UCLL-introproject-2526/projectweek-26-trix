import pygame
import pygame.freetype
import os

WHITE = (255, 255, 255)
DARKBLUE = (149, 219, 242)
LIGHTBLUE = (71, 192, 232)
SELECT_GREEN = (38, 166, 91)
RED_TEXT = (160, 20, 20)   # 🔴 zwaard-tekst
TITLECOLOR = (255, 255, 255)
FPS = 60


def create_text(text, size, color):
    font = pygame.freetype.SysFont("PixelOperator8", size, bold=True)
    surf, _ = font.render(text, color)
    return surf.convert_alpha()


class SwordButton:
    def __init__(self, center, text, sword_img, action=None):
        self.image = sword_img
        self.rect = self.image.get_rect(center=center)

        self.text = text
        self.text_surf = create_text(text, 26, RED_TEXT)  # 🔴 rood
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        self.action = action
        self.hovered = False
        self.selected = False

    def update(self, mouse_pos, mouse_pressed):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_pressed[0] and self.action:
            self.action()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.hovered or self.selected:
            glow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            glow.fill((255, 200, 50, 60))
            screen.blit(glow, self.rect)

        screen.blit(self.text_surf, self.text_rect)


def loadselectionscreen(screen):
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()

    result = None
    running = True

    player1_char = "samurai"
    player2_char = "warrior"
    selected_map = "default"

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 🗡️ Zwaard button
    sword_path = os.path.join(base_dir, "sword_button.png")
    sword_img = pygame.image.load(sword_path).convert_alpha()
    sword_img = pygame.transform.scale(sword_img, (360, 80))

    # 🌄 Achtergrond image
    bg_path = os.path.join(base_dir, "selection_background.png")
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    def set_p1(char):
        nonlocal player1_char
        player1_char = char

    def set_p2(char):
        nonlocal player2_char
        player2_char = char

    def set_map(m):
        nonlocal selected_map
        selected_map = m

    def start_game():
        nonlocal result, running
        result = "start"
        running = False

    def go_back():
        nonlocal result, running
        result = "back"
        running = False

    title = create_text("Kies characters en map", 48, TITLECOLOR)

    characters = ["Samurai", "Warrior"]
    maps = ["default", "map1", "map2"]

    p1_buttons = []
    p2_buttons = []

    start_y = 260
    spacing = 110

    for i, ch in enumerate(characters):
        p1_buttons.append(
            SwordButton(
                (screen_width // 4, start_y + i * spacing),
                ch,
                sword_img,
                action=lambda c=ch.lower(): set_p1(c)
            )
        )

        p2_buttons.append(
            SwordButton(
                (3 * screen_width // 4, start_y + i * spacing),
                ch,
                sword_img,
                action=lambda c=ch.lower(): set_p2(c)
            )
        )

    map_buttons = []
    for i, m in enumerate(maps):
        map_buttons.append(
            SwordButton(
                (screen_width // 2, start_y + i * spacing),
                m.upper(),
                sword_img,
                action=lambda mm=m: set_map(mm)
            )
        )

    start_button = SwordButton(
        (screen_width // 2, screen_height - 160),
        "START",
        sword_img,
        action=start_game
    )

    back_button = SwordButton(
        (screen_width // 2, screen_height - 70),
        "TERUG",
        sword_img,
        action=go_back
    )

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back", player1_char, player2_char, selected_map
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back", player1_char, player2_char, selected_map

        # achtergrond tekenen
        screen.blit(background, (0, 0))

        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 90))

        for b in p1_buttons:
            b.selected = b.text.lower() == player1_char
            b.update(mouse_pos, mouse_pressed)
            b.draw(screen)

        for b in p2_buttons:
            b.selected = b.text.lower() == player2_char
            b.update(mouse_pos, mouse_pressed)
            b.draw(screen)

        for b in map_buttons:
            b.selected = b.text.lower() == selected_map
            b.update(mouse_pos, mouse_pressed)
            b.draw(screen)

        start_button.update(mouse_pos, mouse_pressed)
        start_button.draw(screen)

        back_button.update(mouse_pos, mouse_pressed)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    return result, player1_char, player2_char, selected_map
