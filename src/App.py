import sys
import pygame
from tkinter import Tk

from ImportacoesButton import ImportacoesButton
from LoginApp import LoginApp
from DisplayManager import DisplayManager
from Background import Background
from HomeButton import HomeButton
from RelatorioButton import RelatorioButton
from CreateUserDatabase import DataBase
from TransacoesButton import TransacoesButton
from ImportacoesButton import ImportacoesButton


class App:
    def __init__(self):
        self.background = None
        self.user_name = None
        self.user_surname = None
        pygame.init()
        self.display_manager = None     #   começa em none
        self.login_manager = None
        self.draw_background = None     #   começa em none
        pygame.mixer.init()  # pra começar o audio
        self.db = DataBase()

    def start_login_screen(self):
        root = Tk()

        self.login_manager = LoginApp(root)     # Exibe a tela de login usando Tkinter (nunnca tinha usado, mas está funcionando)
        root.mainloop()  # Aguarda fechar a tela de login

    def run(self):
        self.db.create_table()
        screen = pygame.display.set_mode((1300, 900))
        pygame.display.set_caption("Gerenciamento de Finanças")

        self.background = Background('Data/image/background.jpg', screen)

        self.background.draw()
        pygame.display.flip()  # Atualiza a tela com o background

        self.start_login_screen()

        # Verifica se o login foi bem-sucedido antes de continuar
        if self.login_manager.login_successful:

            self.user_name = self.login_manager.surname
            self.user_surname = self.login_manager.name

            # Inicializa o DisplayManager agora com o nome e sobrenome
            self.display_manager = DisplayManager(self.user_surname, self.user_name)

            # Inicializa o Background usando o display_manager, pois ele já foi criado
            #   self.background = Background(self.display_manager.background_image, self.display_manager.display)
            self.background.draw()
            pygame.display.flip()

            self.main_loop()
        else:
            print("Login falhou.")
            self.quit_game()

    def draw_screen(self, home_button, user_name, user_balance, transactions, transacoes_button):
        self.display_manager.draw_interface()  # Desenha a interface principal

    def main_loop(self):
        screen = pygame.display.set_mode((1300, 900))
        pygame.display.set_caption("Gerenciamento de Finanças")

        font = pygame.font.SysFont("Data/font/Segoe UI Bold.ttf", 58)

        user_full_name = f"{self.user_surname} {self.user_name}"
        user_balance = 2500.50  # Saldo do usuário (isso tem que vir de um banco de dados ou arquivo)
        transactions = [                   # Lista de transações como exemplo
            {'tipo': 'Receita', 'descrição': 'Salário', 'valor': 5000},
            {'tipo': 'Despesa', 'descrição': 'Mercado', 'valor': -300},
            {'tipo': 'Despesa', 'descrição': 'Aluguel', 'valor': -1200}
        ]

        # Se você não tem um ícone, `None` será substituído por uma superfície padrão
        home_button = HomeButton(None, (0, 0), self.display_manager.display, font)
        transacoes_button = TransacoesButton(None, (0, 0), self.display_manager.display,)
        relatorio_button = RelatorioButton(None, (0, 0), self.display_manager.display,)

        self.display_manager.clean_screen()
        self.display_manager.draw_interface()  # Desenha a interface principal
        # [jansen] Descomentei a linha abaixo
        home_button.draw_user_info(user_full_name, user_balance)
        home_button.draw_table(transactions)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.display_manager.check_click(event, self.draw_screen, home_button, user_full_name, user_balance, transactions, transacoes_button)


            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()
