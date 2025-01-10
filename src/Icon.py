import pygame


class Icon:
    def __init__(self, icon, text, pos, display, sound_file):
        self.icon = icon
        self.text = text
        self.pos = pos
        self.display = display
        self.font = pygame.font.Font(None, 35)
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.icon_rect = self.icon.get_rect(topleft=pos)
        self.text_rect = self.text_surface.get_rect(center=(self.icon_rect.centerx, self.icon_rect.bottom + 20))
        self.selected = False
        self.sound_file = sound_file

        self.click_sound = sound_file

        self.rect = self.icon.get_rect(topleft=self.pos)

    def draw(self):
        self.display.blit(self.icon, self.icon_rect.topleft)    # Desenha o icone e o texto
        self.display.blit(self.text_surface, self.text_rect.topleft)

    def play_sound(self):
        if self.click_sound:
            self.click_sound.play()

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.icon_rect.collidepoint(event.pos):
                self.selected = True
                self.play_sound()
            else:
                self.selected = False

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
