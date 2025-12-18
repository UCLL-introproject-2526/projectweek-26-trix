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
    base_dir = os.path.dirname(os.path.abspath(__file__))   # maps/
    project_dir = os.path.dirname(base_dir)                 # project root
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

def generate_map(screen):
    """
    Returns:
      - "menu"     : terug naar menu
      - "restart"  : opnieuw starten
      - "quit"     : afsluiten
    """

<<<<<<< HEAD
=======
    # GEEN pygame.init() hier!
    # GEEN pygame.display.set_mode() hier!
>>>>>>> 2a00415 (update)
    pygame.display.set_caption("Warrior Hills")

    screen_width, screen_height = screen.get_size()

<<<<<<< HEAD
    # Background 
=======
    # Background (maak pad robuust)
>>>>>>> 2a00415 (update)
    base_dir = os.path.dirname(os.path.abspath(__file__))   # maps/
    project_dir = os.path.dirname(base_dir)                 # project root
    bg_path = os.path.join(project_dir, "background.jpg")

    try:
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except Exception as e:
        print("Warning: kon background niet laden:", bg_path, e)
        background = pygame.Surface((screen_width, screen_height))
        background.fill((0, 0, 0))

    clock = pygame.time.Clock()

    # Players
    samurai = Samurai(500, 420)
    warrior = Warrior(100, 385)

    # HP setup
    samurai.max_hp = 100
    samurai.hp = 100
    warrior.max_hp = 100
    warrior.hp = 100

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

        samurai.update(keys)
        warrior.update(keys)

        # Borders
        samurai.clamp_to_screen(screen_width)
        warrior.clamp_to_screen(screen_width)

        # DAMAGE (10 PER HIT)

        if samurai.attack_hitbox and not samurai.damage_applied:
            if samurai.attack_hitbox.colliderect(warrior.hitbox):
                warrior.hp = max(0, warrior.hp - 10)
                samurai.damage_applied = True

        if warrior.attack_hitbox and not warrior.damage_applied:
            if warrior.attack_hitbox.colliderect(samurai.hitbox):
                samurai.hp = max(0, samurai.hp - 10)
                warrior.damage_applied = True

        # GAME OVER
<<<<<<< HEAD
=======
        # -----------------
        if samurai.hp <= 0 or warrior.hp <= 0:
            from end_menu.game_over import game_over  # lazy import ok
            result = game_over(screen)  # moet "restart" of "quit" returnen

            if result == "restart":
                return "restart"
            else:
                return "quit"
>>>>>>> 2a00415 (update)

        if samurai.hp <= 0 or warrior.hp <= 0:
            from end_menu.game_over import game_over  # lazy import ok
            result = game_over(screen)  # moet "restart" of "quit" returnen

            if result == "restart":
                return "restart"
            else:
                return "quit"

        # DRAW

        screen.blit(background, (0, 0))
        samurai.draw(screen)
        warrior.draw(screen)

        # HEALTHBAR OVERLAY
        warrior_key = hp_to_key(warrior.hp)
        samurai_key = hp_to_key(samurai.hp)

        # Warrior: linksboven

        screen.blit(healthbar_images[warrior_key], (20, 20))

        # Samurai: rechtsboven
        
        screen.blit(
            healthbar_images[samurai_key],
            (screen_width - hb_width - 20, 20)
        )

        pygame.display.flip()
        clock.tick(60)

    return "quit"
