import pygame
import os

from Character.samurai import Samurai
from Character.warrior import Warrior

# HEALTHBAR HELPERS
def load_healthbar_frames():
    """
    Laadt healthbars:
    healthbar_0.png, healthbar_10.png, ..., healthbar_100.png
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # maps/
    project_dir = os.path.dirname(base_dir)                # project root
    hb_dir = os.path.join(project_dir, "healthbar")

    frames = {}
    for hp in range(0, 101, 10):
        path = os.path.join(hb_dir, f"healthbar_{hp}.png")
        frames[hp] = pygame.image.load(path).convert_alpha()
    return frames


def hp_to_key(hp):
    """Zet hp om naar 0,10,20,...100"""
    hp = max(0, min(100, hp))
    return (hp // 10) * 10


# MAP / GAME LOOP
def generatemapscreen(screen,
                      player1_char="samurai",
                      player2_char="warrior",
                      selected_map="default"):
    """
    Returns:
    - "menu"   : terug naar menu
    - "restart": opnieuw starten
    - "quit"   : afsluiten
    """
    # GEEN pygame.init() hier!
    # GEEN pygame.display.set_mode() hier!

    pygame.display.set_caption("Warrior Hills")
    screen_width, screen_height = screen.get_size()

    # ---------- BACKGROUND KIEZEN UIT maps/assets ----------
    base_dir = os.path.dirname(os.path.abspath(__file__))   # maps/
    assets_dir = os.path.join(base_dir, "assets")           # maps/assets

    if selected_map == "map1":
        bg_file = "samurai_map.png"              # jouw samurai map
    elif selected_map == "map2":
        bg_file = "bergen.gif.gif"    
    else:
        bg_file = "background.jpg"               # standaard

    bg_path = os.path.join(assets_dir, bg_file)
    print("Background pad:", bg_path)  # debug, mag je later verwijderen

    try:
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except Exception as e:
        print("Warning: kon background niet laden:", bg_path, e)
        background = pygame.Surface((screen_width, screen_height))
        background.fill((0, 0, 0))
    # ------------------------------------------------------

    clock = pygame.time.Clock()

    # Players op basis van keuzes
    if player1_char == "samurai":
        player1 = Samurai(500, 420)
    else:
        player1 = Warrior(500, 385)

    if player2_char == "samurai":
        player2 = Samurai(100, 420)
    else:
        player2 = Warrior(100, 385)

    # HP setup
    player1.max_hp = 100
    player1.hp = 100
    player2.max_hp = 100
    player2.hp = 100

    # Load healthbars
    healthbar_images = load_healthbar_frames()
    hb_width = healthbar_images[100].get_width()

    running = True
    while running:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        keys = pygame.key.get_pressed()

        # UPDATE
        player1.update(keys)
        player2.update(keys)

        # Borders
        player1.clamp_to_screen(screen_width)
        player2.clamp_to_screen(screen_width)

        # DAMAGE (10 PER HIT)
        if player1.attack_hitbox and not player1.damage_applied:
            if player1.attack_hitbox.colliderect(player2.hitbox):
                player2.hp = max(0, player2.hp - 10)
                player1.damage_applied = True

        if player2.attack_hitbox and not player2.damage_applied:
            if player2.attack_hitbox.colliderect(player1.hitbox):
                player1.hp = max(0, player1.hp - 10)
                player2.damage_applied = True

        # GAME OVER
        if player1.hp <= 0 or player2.hp <= 0:
            from end_menu.game_over import game_over  # lazy import ok
            result = game_over(screen)  # moet "restart" of "quit" returnen
            if result == "restart":
                return "restart"
            else:
                return "quit"

        # DRAW
        screen.blit(background, (0, 0))
        player1.draw(screen)
        player2.draw(screen)

        # HEALTHBAR OVERLAY
        p2_key = hp_to_key(player2.hp)
        p1_key = hp_to_key(player1.hp)

        # Player2: linksboven
        screen.blit(healthbar_images[p2_key], (20, 20))

        # Player1: rechtsboven
        screen.blit(
            healthbar_images[p1_key],
            (screen_width - hb_width - 20, 20)
        )

        pygame.display.flip()
        clock.tick(60)

    return "quit"
