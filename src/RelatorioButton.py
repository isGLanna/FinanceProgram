from Button import Button
import pygame
import matplotlib.pyplot as plt
from CreateUserDatabase import *  # Certifique-se de que DataBase está sendo importado corretamente

class RelatorioButton(Button):
    def __init__(self, icon, pos, display):
        if icon is None:
            icon = pygame.Surface((50,50))
            icon.fill((200,200,200))

        super().__init__(icon, pos, display)

        self.font = pygame.font.Font(None, 68)

        self.show_buttons = False
        self.grafico_receitas_button = pygame.Rect(pos[0] + 300, pos[1] - 190, 620, 125)
        self.grafico_despesas_button = pygame.Rect(pos[0] + 300, pos[1] + 100, 630, 125)
        self.quadrado_button = pygame.Rect(pos[0] + 300, pos[1] + 50, 600, 110)

        # Inicialize o banco de dados
        self.db = DataBase()  # Agora self.db estará disponível para as funções de geração de gráficos

    def draw(self):
        if self.show_buttons:
            larger_rect = pygame.Rect(235, 40, 1025, 810)  # Desenha o quadrado grande, igual do button de transacoes
            larger_surface = pygame.Surface(larger_rect.size)
            larger_surface.fill((0, 0, 0))

            black_surface = pygame.Surface(self.display.get_size())
            black_surface.fill((0, 0, 0))
            self.display.blit(black_surface, (200, 0))

            # Desenha o botão de grafico de receitas
            pygame.draw.rect(self.display, (0, 255, 0), self.grafico_receitas_button)
            grafReceitas = self.font.render("Gerar gráfico de Receitas", True, (255, 255, 255))
            self.display.blit(grafReceitas, (self.grafico_receitas_button.x + 20, self.grafico_receitas_button.y + 30))

            # Desenha o botão de grafico de despesas
            pygame.draw.rect(self.display, (255, 0, 0), self.grafico_despesas_button)
            grafDespesas = self.font.render("Gerar gráfico de despesas", True, (255, 255, 255))
            self.display.blit(grafDespesas, (self.grafico_despesas_button.x + 20, self.grafico_despesas_button.y + 30))

    def check_click(self, event, draw_screen, home_button, user_name, user_balance, transactions, transacoes_button):
        if self.rect.collidepoint(event.pos):
            self.show_buttons = True
            draw_screen(home_button, user_name, user_balance, transactions, transacoes_button)
        elif self.show_buttons and self.grafico_receitas_button.collidepoint(event.pos):
            self.generate_grafico_receitas()  # Abre a interface de receitas
        elif self.show_buttons and self.grafico_despesas_button.collidepoint(event.pos):
            self.generate_grafico_despesas()  # Abre a interface de despesas
        else:
            self.show_buttons = False
            draw_screen(home_button, user_name, user_balance, transactions, transacoes_button)

    def generate_grafico_receitas(self):
        # Recupera os dados de receitas do banco de dados
        receitas, limites, meses = self.db.retornar_receitas_totais("Giordano")

        # Extrai os valores para o gráfico
        valores = [r[0] for r in receitas]
        meses = [m[0] for m in meses]

        # Gera o gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(meses, valores, color='green')
        plt.title('Receitas por Mês')
        plt.xlabel('Mês')
        plt.ylabel('Valor (R$)')
        plt.show()

    def generate_grafico_despesas(self):
        # Recupera os dados de despesas do banco de dados
        valores, tipos, dias, descricoes = self.db.retornar_despesas_totais("Giordano")  # Substitua pelo nome do usuário logado

        # Extrai os tipos e valores para o gráfico
        tipos_dict = {}
        for i, tipo in enumerate(tipos):
            if tipo[0] in tipos_dict:
                tipos_dict[tipo[0]] += valores[i][0]
            else:
                tipos_dict[tipo[0]] = valores[i][0]

        # Gera o gráfico
        plt.figure(figsize=(10, 6))
        plt.pie(tipos_dict.values(), labels=tipos_dict.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Despesas por Categoria')
        plt.show()
