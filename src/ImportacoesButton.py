from Button import Button
import pygame
import ImportArchives
from PdfGenerator import *
from ImportArchives import *


class ImportacoesButton(Button):
    def __init__(self, icon, pos, display):

        if icon is None:
            icon = pygame.Surface((50,50))
            icon.fill((200,200,200))

        super().__init__(icon, pos, display)

        self.font = pygame.font.Font(None, 68)

        self.show_buttons = False
        self.importar_button = pygame.Rect(pos[0] + 279, pos[1] - 190, 500, 110)
        self.exportar_button = pygame.Rect(pos[0] + 300, pos[1] + 100, 500, 110)
        self.quadrado_button = pygame.Rect(pos[0] + 300, pos[1] + 50, 600, 110)

        def draw(self):
            if self.show_buttons:
                larger_rect = pygame.Rect(235, 40, 1025, 810)  # Desenha o quadrado grande, igual do button de transacoes
                larger_surface = pygame.Surface(larger_rect.size)
                larger_surface.fill((0, 0, 0))

                black_surface = pygame.Surface(self.display.get_size())
                black_surface.fill((0, 0, 0))
                self.display.blit(black_surface, (200, 0))

                # Desenha o botão de importa
                pygame.draw.rect(self.display, (0, 255, 0), self.importar_button)
                import_text = self.font.render("Importar Receitas e Despesas", True, (255, 255, 255))
                self.display.blit(import_text, (self.receitas_button.x + 20, self.receitas_button.y + 30))

                # Desenha o botão de exporta
                pygame.draw.rect(self.display, (255, 0, 0), self.exportar_button)
                export_text = self.font.render("Exportar dados - .PDF", True, (255, 255, 255))
                self.display.blit(export_text, (self.despesas_button.x + 20, self.despesas_button.y + 30))

    def check_click(self, event, draw_screen, home_button, user_name, user_balance, transactions, transacoes_button):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.show_buttons = not self.show_buttons
                draw_screen(home_button, user_name, user_balance, transactions, transacoes_button)
            elif self.show_buttons:
                if self.importar_button.collidepoint(event.pos):
                    self.show_import_interface()              # Abre a interface de receitas

                elif self.exportar_button.collidepoint(event.pos):
                    self.show_export_interface()              # Abre a interface de despesas

    def show_import_interface(self):
        import_dialog = ImportArchives('csv', "user_name")  # "user_name" tem que vir do banco de dados...
        import_dialog.import_csv()

    def show_export_interface(self):
        export_pdf = PdfFile('user_name')  # username tem que vir do banco de dados tb
        export_pdf.write_document()
