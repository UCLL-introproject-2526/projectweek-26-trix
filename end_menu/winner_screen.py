import pygame
import pygame.freetype
import os


def winner_screen(screen, winner_player: int, winner_image: pygame.Surface):
    w, h = screen.get_size()
    clock = pygame.time.Clock()

    base_dir = os.path.dirname(os.path.abspath(__file__))  # end_menu/
    images_dir = os.path.join(base_dir, "assets", "images")

    bg_path = os.path.join(images_dir, "game_over_screen.png")
    bg = None
    try:
        if os.path.exists(bg_path):
            bg = pygame.image.load(bg_path).convert()
            bg = pygame.transform.scale(bg, (w, h))
    except Exception:
        bg = None

    font_title = pygame.freetype.SysFont("PixelOperator8", max(28, int(h * 0.08)), bold=True)
    font_btn = pygame.freetype.SysFont("PixelOperator8", max(20, int(h * 0.05)), bold=True)

    title_text = f"PLAYER {winner_player} VICTORY"

    def make_button(center, text):
        surf, _ = font_btn.render(text, fgcolor=(255, 255, 255))
        rect = surf.get_rect(center=center)
        pad = 18
        box = rect.inflate(pad * 3, pad * 2)
        return {"text": text, "surf": surf, "rect": rect, "box": box}

    btn_restart = make_button((w // 2, int(h * 0.72)), "RESTART")
    btn_menu = make_button((w // 2, int(h * 0.82)), "MENU")
    btn_quit = make_button((w // 2, int(h * 0.92)), "QUIT")
    buttons = [btn_restart, btn_menu, btn_quit]

    # winner sprite mooi schalen
    champ = winner_image
    try:
        if champ.get_width() > 0:
            target_h = int(h * 0.60)
            scale = target_h / champ.get_height()
            champ = pygame.transform.scale(
                champ, (int(champ.get_width() * scale), int(champ.get_height() * scale))
            )
    except Exception:
        pass

    champ_rect = champ.get_rect(center=(w // 2, int(h * 0.42)))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((0, 0, 0))

        title_surf, _ = font_title.render(title_text, fgcolor=(255, 215, 0))
        screen.blit(title_surf, (w // 2 - title_surf.get_width() // 2, int(h * 0.10)))

        screen.blit(champ, champ_rect)

        for b in buttons:
            hovered = b["box"].collidepoint(mouse_pos)

            color = (255, 255, 255) if hovered else (220, 220, 220)
            border = (255, 215, 0) if hovered else (149, 219, 242)

            pygame.draw.rect(screen, (40, 40, 40), b["box"], border_radius=10)
            pygame.draw.rect(screen, border, b["box"], width=3, border_radius=10)

            # re-render text met hover kleur
            txt, _ = font_btn.render(b["text"], fgcolor=color)
            txt_rect = txt.get_rect(center=b["box"].center)
            screen.blit(txt, txt_rect)

            if hovered and mouse_pressed[0]:
                if b["text"] == "RESTART":
                    return "restart"
                if b["text"] == "MENU":
                    return "menu"
                return "quit"

        pygame.display.flip()
        clock.tick(60)

    return "quit"
