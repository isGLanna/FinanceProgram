import pygame

class Background:
    def __init__(self, image_path, display):
        self.display = display
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.smoothscale(self.image, (display.get_width(), display.get_height()))

    def draw(self):
        self.display.blit(self.image, (0, 0))
