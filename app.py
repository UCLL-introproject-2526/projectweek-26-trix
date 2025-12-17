import pygame

def create_main_surface():
    screen_size = (1024, 786)
    return pygame.display.set_mode(screen_size)

def clear_surface(surface):
    surface.fill((0, 0, 0))

def render_frame(surface, x):
    pygame.draw.circle(
        surface, (255, 0, 0), (x, 393), 50
    )
    pygame.display.flip()

def main():
    pygame.init()
    surface = create_main_surface()

    x = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"A key was pressed! Key code: {event.key}")

        render_frame(surface, x)
        x += 1

    pygame.quit()

main()