import pygame
from HomeButton import HomeButton
from Icon import Icon
from ImportacoesButton import ImportacoesButton
from RelatorioButton import RelatorioButton
from TransacoesButton import TransacoesButton
from ButtonManager import ButtonManager


class DisplayManager:
    def __init__(self, user_name, user_surname, user_balance=2500.50):
        self.icons = None
        self.user_name = f"{user_name} {user_surname}"
        self.user_balance = user_balance

        pygame.init()
        pygame.mixer.init()

        self.height = 900
        self.width = 1300
        self.display = pygame.display.set_mode((self.width, self.height))
        self.font_0 = pygame.font.Font("Data/font/Segoe UI Bold.ttf", 58)
        self.clock = pygame.time.Clock()
        self.background_image = "Data/image/background.jpg"
        self.sound_click = pygame.mixer.Sound("Data/sound/som_clique.wav")
        self.sound_click.set_volume(0.5)

        # Carregar imagens e ícones
        self.button1_image = pygame.image.load('Data/image/button1.png').convert_alpha()
        self.icone_home = pygame.image.load('Data/image/icone_home.png').convert_alpha()
        self.icone_transacoes = pygame.image.load('Data/image/icone_transacoes.png').convert_alpha()
        self.icone_relatorios = pygame.image.load('Data/image/icone_relatorios.png').convert_alpha()
        self.icone_importacoes = pygame.image.load('Data/image/icone_importacoes.png').convert_alpha()

        # Instanciar o botão Home
        self.home_button = HomeButton(self.icone_home, (70, 190), self.display, self.font_0)
        self.transacoes_button = TransacoesButton(self.icone_transacoes, (70, 370), self.display)
        self.relatorio_button = RelatorioButton(self.icone_relatorios, (70, 550), self.display)
        self.importacoes_button = ImportacoesButton(self.icone_importacoes, (70, 730), self.display)

        self.button_manager = ButtonManager()

        self.button_manager.add_button(self.home_button)
        self.button_manager.add_button(self.transacoes_button)
        self.button_manager.add_button(self.relatorio_button)
        self.button_manager.add_button(self.importacoes_button)

        #   self.home_button.clicked = True
        self.buttons = [self.home_button, self.transacoes_button, self.relatorio_button, self.importacoes_button]

    def clean_screen(self):
        # [jansen]
        self.display.fill((0, 0, 0))

    def draw_interface(self):
        # [jansen] self.display.fill((0, 0, 0))

        # Desenhar as informações do usuário e saldo no HomeButton
        # [jansen] self.home_button.draw_user_info(self.user_name, self.user_balance)

        # [jansen] pygame.display.flip()

        # Desenha os ícones
        home_icon = Icon(self.icone_home, "Home", (70, 190), self.display, self.sound_click)
        transacoes_icon = Icon(self.icone_transacoes, "Transações", (70, 370), self.display, self.sound_click)
        relatorios_icon = Icon(self.icone_relatorios, "Relatórios", (70, 550), self.display, self.sound_click)
        importacoes_icon = Icon(self.icone_importacoes, "Importações", (70, 730), self.display,self.sound_click)

        self.icons = [home_icon, transacoes_icon, relatorios_icon, importacoes_icon]
        for icon in self.icons:
            icon.draw()

        self.home_button.draw()
        self.transacoes_button.draw()
        self.relatorio_button.draw()
        self.importacoes_button.draw()
        pygame.display.flip()

    # DisplayManager.py
    def check_click(self, event, drawScreen, home_button, user_name, user_balance, transactions, transacoes_button):
        self.home_button.check_click(event, drawScreen, home_button, user_name, user_balance, transactions, transacoes_button)
        self.transacoes_button.check_click(event, drawScreen, home_button, user_name, user_balance, transactions, transacoes_button)
        self.relatorio_button.check_click(event, drawScreen, home_button, user_name, user_balance, transactions, transacoes_button)
        self.importacoes_button.check_click(event, drawScreen, home_button, user_name, user_balance, transactions, transacoes_button)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for icon in self.icons:
                if icon.rect.collidepoint(event.pos):
                    icon.play_sound()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for icon in self.icons:
                if icon.rect.collidepoint(event.pos):
                    icon.play_sound()
