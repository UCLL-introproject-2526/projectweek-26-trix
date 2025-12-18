import pygame
import os

from controls import P1, P2
from Character.samurai import Samurai
from Character.warrior import Warrior
from Character.huntress import Huntress
from Character.king import King
from Character.martial_hero import MartialHero
from Character.martial_hero2 import MartialHero2


def load_healthbar_frames():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # maps/
    project_dir = os.path.dirname(base_dir)                # project root
    hb_dir = os.path.join(project_dir, "healthbar")

    frames = {}
    for hp in range(0, 101, 10):
        path = os.path.join(hb_dir, f"healthbar_{hp}.png")
        frames[hp] = pygame.image.load(path).convert_alpha()
    return frames


def hp_to_key(hp):
    hp = max(0, min(100, hp))
    return (hp // 10) * 10


def compute_spawn_y(PlayerClass, desired_hitbox_bottom_y, controls):
    # Some player classes accept a `controls` argument in __init__, others do not.
    # Try instantiating with controls first, fall back to without.
    try:
        tmp = PlayerClass(0, 0, controls)
    except TypeError:
        tmp = PlayerClass(0, 0)

    dy = tmp.hitbox.y - tmp.rect.y
    hb_h = tmp.hitbox.height
    return int(desired_hitbox_bottom_y - (dy + hb_h))


def instantiate_player(PlayerClass, x, y, controls):
    """Instantiate PlayerClass with or without controls depending on signature."""
    try:
        return PlayerClass(x, y, controls)
    except TypeError:
        return PlayerClass(x, y)


def generatemapscreen(screen,
                      player1_char="samurai",
                      player2_char="warrior",
                      selected_map="default"):
    pygame.display.set_caption("Warrior Hills")
    screen_width, screen_height = screen.get_size()

    base_dir = os.path.dirname(os.path.abspath(__file__))   # .../maps
    assets_dir = os.path.join(base_dir, "assets")           # .../maps/assets

    if selected_map == "map1":
        bg_file = "samurai_map.png"              # of .jpg, precies zoals bestand heet
    elif selected_map == "map2":
        bg_file = "bergen.gif.gif"                   # als het echt zo heet, zonder extra .gif
    else:
        bg_file = "background.jpg"               # standaard

    bg_path = os.path.join(assets_dir, bg_file)
    print("Background pad:", bg_path)
  # debug, mag je later verwijderen

    try:
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except Exception as e:
        print("Warning: kon background niet laden:", bg_path, e)
        background = pygame.Surface((screen_width, screen_height))
        background.fill((0, 0, 0))
    # ------------------------------------------------------

    clock = pygame.time.Clock()

    floor_hitbox_bottom = int(screen_height * 0.90)

    # --- AANPASBAAR: zet players lager/hoger ---
    # positief = lager (naar beneden), negatief = hoger
    p1_y_offset = 110
    p2_y_offset = 110
    # ------------------------------------------

    p1_x = int(screen_width * 0.20)
    p2_x = int(screen_width * 0.80)

    if player1_char == "samurai":
        p1_y = compute_spawn_y(Samurai, floor_hitbox_bottom + p1_y_offset, P1)
        player1 = instantiate_player(Samurai, p1_x, p1_y, P1)
    elif player1_char == "warrior":
        p1_y = compute_spawn_y(Warrior, floor_hitbox_bottom, P1)
        player1 = instantiate_player(Warrior, p1_x, p1_y, P1)
    elif player1_char == "huntress":
        p1_y = compute_spawn_y(Huntress, floor_hitbox_bottom, P1)
        player1 = instantiate_player(Huntress, p1_x, p1_y, P1)
    elif player1_char == "king":
        p1_y = compute_spawn_y(King, floor_hitbox_bottom, P1)
        player1 = instantiate_player(King, p1_x, p1_y, P1)
    elif player1_char == "martial_hero":
        p1_y = compute_spawn_y(MartialHero, floor_hitbox_bottom, P1)
        player1 = instantiate_player(MartialHero, p1_x, p1_y, P1)
    elif player1_char == "martial_hero2":
        p1_y = compute_spawn_y(MartialHero2, floor_hitbox_bottom, P1)
        player1 = instantiate_player(MartialHero2, p1_x, p1_y, P1)

    if player2_char == "samurai":
        p2_y = compute_spawn_y(Samurai, floor_hitbox_bottom + p2_y_offset, P2)
        player2 = instantiate_player(Samurai, p2_x, p2_y, P2)
    elif player2_char == "warrior":
        p2_y = compute_spawn_y(Warrior, floor_hitbox_bottom, P2)
        player2 = instantiate_player(Warrior, p2_x, p2_y, P2)
    elif player2_char == "huntress":
        p2_y = compute_spawn_y(Huntress, floor_hitbox_bottom, P2)
        player2 = instantiate_player(Huntress, p2_x, p2_y, P2)
    elif player2_char == "king":
        p2_y = compute_spawn_y(King, floor_hitbox_bottom, P2)
        player2 = instantiate_player(King, p2_x, p2_y, P2)
    elif player2_char == "martial_hero":
        p2_y = compute_spawn_y(MartialHero, floor_hitbox_bottom, P2)
        player2 = instantiate_player(MartialHero, p2_x, p2_y, P2)
    elif player2_char == "martial_hero2":
        p2_y = compute_spawn_y(MartialHero2, floor_hitbox_bottom, P2)
        player2 = instantiate_player(MartialHero2, p2_x, p2_y, P2)

    player1.max_hp = 100
    player1.hp = 100
    player2.max_hp = 100
    player2.hp = 100

    healthbar_images = load_healthbar_frames()
    hb_width = healthbar_images[100].get_width()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        keys = pygame.key.get_pressed()

        player1.update(keys)
        player2.update(keys)

        player1.clamp_to_screen(screen_width)
        player2.clamp_to_screen(screen_width)

        if player1.attack_hitbox and not player1.damage_applied:
            if player1.attack_hitbox.colliderect(player2.hitbox):
                player2.hp = max(0, player2.hp - 10)
                player1.damage_applied = True

        if player2.attack_hitbox and not player2.damage_applied:
            if player2.attack_hitbox.colliderect(player1.hitbox):
                player1.hp = max(0, player1.hp - 10)
                player2.damage_applied = True

        if player1.hp <= 0 or player2.hp <= 0:
            from end_menu.game_over import game_over
            result = game_over(screen)
            return "restart" if result == "restart" else "quit"

        screen.blit(background, (0, 0))
        player1.draw(screen)
        player2.draw(screen)

        p2_key = hp_to_key(player2.hp)
        p1_key = hp_to_key(player1.hp)

        screen.blit(healthbar_images[p2_key], (20, 20))
        screen.blit(
            healthbar_images[p1_key],
            (screen_width - hb_width - 20, 20)
        )

        pygame.display.flip()
        clock.tick(60)

    return "quit"
