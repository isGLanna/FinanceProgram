from Button import Button
import pygame


class HomeButton(Button):
    def __init__(self, icon, pos, display, font):

        if icon is None:  # Se o ícone for None, crie um ícone de placeholder(parece dar certo, coisa nova)
            icon = pygame.Surface((50, 50))  # Cria uma superfície
            icon.fill((200, 200, 200))  # Preenche com cinza

        super().__init__(icon, pos, display)
        self.font = font

    def draw_user_info(self, user_name, user_balance):
        user_name_text = self.font.render(f"Seja Bem-vindo(a), {user_name}.", True, (255, 255, 255))  # Cor branca
        self.display.blit(user_name_text, (350, 100))  # Exibe o nome na posição (50, 50)

        balance_text = self.font.render(f"Saldo Atual: R$ {user_balance:.2f}", True, (255, 255, 255))  # Cor branca
        self.display.blit(balance_text, (350, 150))  # Exibe o saldo na posição (50, 100)

    def check_click(self, event, drawScreen, home_button, user_name, user_balance, transactions, transacoes_button):

        if self.rect.collidepoint(event.pos):
            self.display.fill((0, 0, 0))

            home_button.draw_user_info(user_name,
                                       user_balance)  # Chama o metodo draw do transacoes_button para desenhar os botões

            home_button.draw_table(transactions)
            #   drawScreen()                           # Atualiza a tela
            print("HomeButton foi clicado e a tela de transações ta printada.")

    def draw_table(self, transactions):
        """
        Esta função desenha uma tabela simples com as descrições das receitas e despesas.

        :param transactions: Lista de dicionários com as transações. Exemplo:
            [
                {'tipo': 'Receita', 'descrição': 'Salário', 'valor': 5000},
                {'tipo': 'Despesa', 'descrição': 'Mercado', 'valor': -300},
            ]
        """
        y_offset = 500
        for transaction in transactions:
            text = f"{transaction['tipo']}: {transaction['descrição']} - R$ {transaction['valor']:.2f}"
            text_surface = self.font.render(text, True, (255, 255, 255))  # Cor branca
            self.display.blit(text_surface, (350, y_offset))
            y_offset += 100  # Move para a próxima linha

