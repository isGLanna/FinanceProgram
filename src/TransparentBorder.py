import pygame

class TransparentBorder:
    def __init__(self, icon, border_color=(255, 255, 255, 120), border_size=(50, 60)):
        self.icon = icon
        self.border_color = border_color
        self.border_size = border_size
        self.rect = self.icon.get_rect()

    def draw(self, display, pos):
        self.rect.topleft = pos

        border_surface = pygame.Surface((self.rect.width + self.border_size[0], self.rect.height + self.border_size[1]), pygame.SRCALPHA)   # Desenha a borda transparente ao redor do ícone
        border_surface.fill(self.border_color)
        display.blit(border_surface, (self.rect.x - self.border_size[0] // 2, self.rect.y - self.border_size[1] // 2))

        larger_rect = pygame.Rect(235, 40, 800, 810)   # Quadrado grande transparente (posição fixa)
        larger_surface = pygame.Surface(larger_rect.size, pygame.SRCALPHA)
        larger_surface.fill((255, 255, 255, 80))
        display.blit(larger_surface, larger_rect.topleft)

        # Desenha o ícone sobre a borda e o quadrado transparente
        display.blit(self.icon, pos)
