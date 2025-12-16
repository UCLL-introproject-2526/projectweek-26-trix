import pygame
import sys

pygame.init()

# ================== CONFIG ==================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

TILE_SIZE = 16          # exact zoals je tileset
TILES_PER_ROW = 16      # 16 x 16 = 256 tiles

TILESET_PATH = "image_with_grid.png"

# ================== SETUP ==================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("16x16 Tile Map – Numeric IDs")
clock = pygame.time.Clock()

# ================== LOAD TILESET ==================
tileset = pygame.image.load(TILESET_PATH).convert_alpha()

tiles = []  # index = tile ID (0–255)

for row in range(TILES_PER_ROW):
    for col in range(TILES_PER_ROW):
        tile_id = row * TILES_PER_ROW + col
        rect = pygame.Rect(
            col * TILE_SIZE,
            row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
        tile = tileset.subsurface(rect)
        tiles.append(tile)

print("Tiles geladen:", len(tiles))  # moet 256 zijn

# ================== MAP MET CIJFERS ==================
# -1 = leeg
# 0..255 = tile ID uit tileset

game_map = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0, 17, 18, 19, 20, 21, 22,  0],
    [ 0, 33, 34, 35, 36, 37, 38,  0],
    [ 0, 49, 50, 51, 52, 53, 54,  0],
    [ 0, 65, 66, 67, 68, 69, 70,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
]

# ================== MAIN LOOP ==================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # Map tekenen
    for row in range(len(game_map)):
        for col in range(len(game_map[0])):
            tile_id = game_map[row][col]
            if tile_id >= 0:
                screen.blit(
                    tiles[tile_id],
                    (col * TILE_SIZE, row * TILE_SIZE)
                )

    pygame.display.flip()
    clock.tick(60)
