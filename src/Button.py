import pygame
from TransparentBorder import TransparentBorder

class Button:
    def __init__(self, icon, pos, display, border_color=(255, 255, 255, 120), border_size=(55, 68)):
        self.icon = icon
        self.pos = pos
        self.display = display
        self.rect = self.icon.get_rect(topleft=pos)
        self.clicked = False
        self.border = TransparentBorder(icon, border_color, border_size)
        self.manager = None

    def draw(self):
        if self.clicked:
            self.border.draw(self.display , self.pos)
        self.display.blit(self.icon, self.pos)

    def check_click(self, event, drawScreen, home_button, user_name, user_balance, transactions, transacoes_button):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.manager:
                    drawScreen(home_button, user_name, user_balance, transactions, transacoes_button)
                    self.manager.button_clicked(self)
                else:
                    self.clicked = not self.clicked

    def set_manager(self, manager):
        self.manager = manager

    def select(self):
        self.clicked = True

    def deselect(self):
        self.clicked = False
