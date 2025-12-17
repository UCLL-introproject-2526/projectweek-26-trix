import os
import pygame

def load_images(path):
    images = []
    for file in sorted(os.listdir(path)):
        if file.lower().endswith(".png"):
            img = pygame.image.load(os.path.join(path, file)).convert_alpha()
            images.append(img)
    return images