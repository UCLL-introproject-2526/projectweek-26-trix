import pygame
import os
import pygame.freetype


def _scale_to_height(img, target_h):
    scale = target_h / img.get_height()
    return pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))


def _load_frames(images_dir, prefix, count=10):
    frames = []
    for i in range(count):
        path = os.path.join(images_dir, f"{prefix}_{i}.png")
        if os.path.exists(path):
            frames.append(pygame.image.load(path).convert_alpha())
    return frames


def game_over(screen, winner_player=1, winner_char=None, winner_image=None):
    w, h = screen.get_size()
    pygame.display.set_caption("Victory")

    base_dir = os.path.dirname(os.path.abspath(__file__))   # end_menu/
    images_dir = os.path.join(base_dir, "assets", "images")

    winner_char = (winner_char or "").lower().strip()

    bg_path = os.path.join(images_dir, "selection_background.png")
    try:
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (w, h))
    except Exception:
        background = pygame.Surface((w, h))
        background.fill((0, 0, 0))

    restart_path = os.path.join(images_dir, "restart_sword.png")
    quit_path = os.path.join(images_dir, "quit_sword.png")

    try:
        restart_surface = pygame.image.load(restart_path).convert_alpha()
        quit_surface = pygame.image.load(quit_path).convert_alpha()
    except Exception as e:
        print("kon knoppen niet laden:", e)
        return "quit"

    restart_rect = restart_surface.get_rect(midtop=(w // 2, int(h * 0.68)))
    quit_rect = quit_surface.get_rect(midtop=(w // 2, int(h * 0.68) + 120))

    font = pygame.freetype.SysFont("PixelOperator8", max(30, int(h * 0.08)), bold=True)
    title_text = f"PLAYER {winner_player} VICTORY"
    title_surf, _ = font.render(title_text, fgcolor=(255, 215, 0))
    title_rect = title_surf.get_rect(center=(w // 2, int(h * 0.18)))

    target_h = int(h * 0.30)

    anim_frames = []
    if winner_char == "samurai":
        anim_frames = _load_frames(images_dir, "samurai", 10)
    elif winner_char == "warrior":
        anim_frames = _load_frames(images_dir, "warrior", 10)

    if anim_frames:
        anim_frames = [_scale_to_height(f, target_h) for f in anim_frames]

    champ = None
    if anim_frames:
        champ = anim_frames[0]
    elif winner_image is not None:
        try:
            champ = _scale_to_height(winner_image, target_h)
        except Exception:
            champ = None

    if champ is None:
        champ = pygame.Surface((int(w * 0.18), int(h * 0.28)), pygame.SRCALPHA)
        champ.fill((255, 0, 0, 120))

    champ_rect = champ.get_rect(center=(w // 2, int(h * 0.42)))

    clock = pygame.time.Clock()
    frame_i = 0
    frame_timer = 0.0
    frame_time = 0.09

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_a:
                    return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                if quit_rect.collidepoint(event.pos):
                    return "quit"
        # mannetje laten zien in eind scherm als winnaar
        if anim_frames:
            frame_timer += dt
            if frame_timer >= frame_time:
                frame_timer = 0.0
                frame_i = (frame_i + 1) % len(anim_frames)
            champ = anim_frames[frame_i]
            champ_rect = champ.get_rect(center=(w // 2, int(h * 0.42)))

        screen.blit(background, (0, 0))
        screen.blit(title_surf, title_rect)
        screen.blit(champ, champ_rect)
        screen.blit(restart_surface, restart_rect)
        screen.blit(quit_surface, quit_rect)

        pygame.display.flip()
