import pygame
import sys

pygame.init()

# ================== CONFIG ==================
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

TILE_SIZE = 16
TILES_PER_ROW = 16

MAP_COLS = SCREEN_WIDTH // TILE_SIZE   # 120
MAP_ROWS = SCREEN_HEIGHT // TILE_SIZE  # 67

TILESET_PATH = "image_with_grid.png"
FILL_TILE_ID = 0  # standaard blok (bijv. gras)

# ================== MAP CONFIG (wijzig in de code) ==================
# Pas deze waarden aan in de code om de gegenereerde wereld te veranderen.
SKY_TILE = 192
MOUNTAIN_TILE = 1
GROUND_TILE = 16
UNDERGROUND_TILE = 2
# ================== ROW DEFINITIE (wijzig hier de lagen)
# Elke entry in `ROW_TILES` correspondeert met één rij (horizontaal) in de map.
# Zet hier rechtstreeks de tile-id die die hele rij moet krijgen.
# Voorbeeld: bovenste 20 rijen lucht, volgende 40 rijen grond, onderste rijen ondergrond:
ROW_TILES = [SKY_TILE]*55 + [FILL_TILE_ID]*1 + [GROUND_TILE]*50 
# Standaard: begin volledig met lucht (lege/sky achtergrond)
#ROW_TILES = [SKY_TILE] * MAP_ROWS

# Hulpfunctie (optioneel) om een range van rijen te vullen vanuit code
def fill_row_range(start_row, end_row, tile_id):
    """Vul rijen [start_row, end_row) met tile_id."""
    for i in range(max(0, start_row), min(MAP_ROWS, end_row)):
        ROW_TILES[i] = tile_id

# Voorbeeld (commented):
# fill_row_range(0, 20, SKY_TILE)
# fill_row_range(20, 60, GROUND_TILE)
# fill_row_range(60, MAP_ROWS, UNDERGROUND_TILE)

# ================== FULL-SCREEN MAP GENERATIE ==================
# Genereer de volledige kaart in de code zodat de wereld direct fullscreen is
# Wijzig de constants bovenaan om het uiterlijk te veranderen.
def generate_fullscreen_map():
    m = []
    for r in range(MAP_ROWS):
        row = []
        for c in range(MAP_COLS):
            # gebruik de tile-id die in ROW_TILES voor deze rij staat
            # (geen patronen — elke rij is uniform)
            if r < len(ROW_TILES):
                tid = ROW_TILES[r]
            else:
                tid = FILL_TILE_ID
            row.append(tid)
        m.append(row)
    return m

game_map = generate_fullscreen_map()

# ================== SETUP ==================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("1920x1080 Tile Map – Manual Numeric System")
clock = pygame.time.Clock()

# ================== LOAD TILESET ==================
tileset = pygame.image.load(TILESET_PATH).convert_alpha()

tiles = []
for r in range(TILES_PER_ROW):
    for c in range(TILES_PER_ROW):
        rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tiles.append(tileset.subsurface(rect))

print("Tiles geladen:", len(tiles))  # 256

# ================== MAIN LOOP ==================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    for r in range(MAP_ROWS):
        for c in range(MAP_COLS):
            tile_id = game_map[r][c]
            if tile_id >= 0:
                screen.blit(
                    tiles[tile_id],
                    (c * TILE_SIZE, r * TILE_SIZE)
                )

    # (Runtime editing disabled) Pas `MAP CONFIG` bovenaan aan en herstart de game.

    pygame.display.flip()
    clock.tick(60)
