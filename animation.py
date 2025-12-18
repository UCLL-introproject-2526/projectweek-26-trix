class Animation:
    def __init__(self, images, speed, loop=True):
        self.images = images
        self.speed = speed
        self.loop = loop
        self.index = 0.0

    def reset(self):
        self.index = 0.0

    def finished(self):
        return int(self.index) >= len(self.images) - 1

    def update(self):
        if len(self.images) == 0:
            return

        # Als niet-loopend en al klaar: blijf op laatste frame
        if not self.loop and self.finished():
            self.index = float(len(self.images) - 1)
            return

        self.index += self.speed

        if self.index >= len(self.images):
            if self.loop:
                self.index = 0.0
            else:
                self.index = float(len(self.images) - 1)

    def get_image(self):
        if len(self.images) == 0:
            return None
        return self.images[int(self.index)]
