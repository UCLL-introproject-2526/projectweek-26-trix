class Animation:
    def __init__(self, images, speed):
        self.images = images
        self.speed = speed
        self.index = 0

    def update(self):
        self.index += self.speed
        if self.index >= len(self.images):
            self.index = 0

    def get_image(self):
        return self.images[int(self.index)]
