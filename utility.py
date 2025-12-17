import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_images(relative_path):
    images = []
    full_path = os.path.join(BASE_DIR, relative_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Map niet gevonden: {full_path}")

    for file in sorted(os.listdir(full_path)):
        if file.lower().endswith(".png"):
            img = pygame.image.load(os.path.join(full_path, file)).convert_alpha()
            images.append(img)

    return images
