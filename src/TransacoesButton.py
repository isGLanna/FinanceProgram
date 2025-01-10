"""nessa classe precisamos exibir 2 botões para entradas de valores, um para receita e outro para despesas
   e também para escolher entre as categorias/descrição das atividades
   ex de categorias:
   receitas: salário, pix, outras receitas
   despesas: outros, mercado, alimentação, restaurante, casa, educação, família, impostos,
   pets, presentes, roupas, saúde, viagem, trabalho, transporte, compras    """


import pygame
from tkinter import Tk, Label, Entry, Button as TkButton, messagebox
from threading import Thread
from Button import Button
from CreateUserDatabase import DataBase

class TransacoesButton(Button):
    def __init__(self, icon, pos, display):
        if icon is None:
            icon = pygame.Surface((50, 50))
            icon.fill((200, 200, 200))
        self.db = DataBase()

        super().__init__(icon, pos, display)

        self.show_buttons = False
        self.receitas_button = pygame.Rect(pos[0] + 300, pos[1] - 190, 500, 110)  # Botão para receitas
        self.despesas_button = pygame.Rect(pos[0] + 300, pos[1] + 100, 500, 110)  # Botão para despesas
        self.quadrado_button = pygame.Rect(pos[0] + 300, pos[1] + 50, 600, 110)
        self.font = pygame.font.Font(None, 68)

    def draw(self):
        if self.show_buttons:
            larger_rect = pygame.Rect(235, 40, 1025, 810)           # Desenha o quadrado grande
            larger_surface = pygame.Surface(larger_rect.size)
            larger_surface.fill((0, 0, 0))

            black_surface = pygame.Surface(self.display.get_size())
            black_surface.fill((0, 0, 0))
            self.display.blit(black_surface, (200, 0))

            # Desenha o botão de receitas
            pygame.draw.rect(self.display, (0, 255, 0), self.receitas_button)
            receita_text = self.font.render("Adicionar Receitas", True, (255, 255, 255))
            self.display.blit(receita_text, (self.receitas_button.x + 20, self.receitas_button.y + 30))

            # Desenha o botão de despesas
            pygame.draw.rect(self.display, (255, 0, 0), self.despesas_button)
            despesas_text = self.font.render("Adicionar Despesas", True, (255, 255, 255))
            self.display.blit(despesas_text, (self.despesas_button.x + 20, self.despesas_button.y + 30))

    def check_click(self, event, draw_screen, home_button, user_name, user_balance, transactions, transacoes_button):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.show_buttons = True
                draw_screen(home_button, user_name, user_balance, transactions, transacoes_button)
            elif self.show_buttons and self.receitas_button.collidepoint(event.pos):
                self.show_receitas_interface()
            elif self.show_buttons and self.despesas_button.collidepoint(event.pos):
                self.show_despesas_interface()
            else:
                self.show_buttons = False
                draw_screen(home_button, user_name, user_balance, transactions, transacoes_button)

    def show_receitas_interface(self):
        def run_tk():
            root = Tk()
            root.title("Inserir Receita")

            Label(root, text="Categoria:").grid(row=0, column=0, padx=10, pady=10)
            categoria_entry = Entry(root)
            categoria_entry.grid(row=0, column=1, padx=10, pady=10)

            Label(root, text="Valor:").grid(row=1, column=0, padx=10, pady=10)
            valor_entry = Entry(root)
            valor_entry.grid(row=1, column=1, padx=10, pady=10)

            def inserir_receita():
                categoria = categoria_entry.get()
                valor = valor_entry.get()
                if categoria and valor:
                    try:
                        valor = float(valor)
                        self.inserir_no_banco('receita', categoria, valor)
                        messagebox.showinfo("Sucesso", "Receita adicionada com sucesso!")
                        root.destroy()
                    except ValueError:
                        messagebox.showerror("Erro", "Valor deve ser numérico.")
                else:
                    messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

            TkButton(root, text="Adicionar Receita", command=inserir_receita).grid(row=2, column=0, columnspan=2, pady=10)

            root.mainloop()

        Thread(target=run_tk).start()

    def show_despesas_interface(self):
        def run_tk():
            root = Tk()
            root.title("Inserir Despesa")

            Label(root, text="Categoria:").grid(row=0, column=0, padx=10, pady=10)
            categoria_entry = Entry(root)
            categoria_entry.grid(row=0, column=1, padx=10, pady=10)

            Label(root, text="Valor:").grid(row=1, column=0, padx=10, pady=10)
            valor_entry = Entry(root)
            valor_entry.grid(row=1, column=1, padx=10, pady=10)

            def inserir_despesa():
                categoria = categoria_entry.get()
                valor = valor_entry.get()
                if categoria and valor:
                    try:
                        valor = float(valor)
                        self.inserir_no_banco('despesa', categoria, valor)
                        messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
                        root.destroy()
                    except ValueError:
                        messagebox.showerror("Erro", "Valor deve ser numérico.")
                else:
                    messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

            TkButton(root, text="Adicionar Despesa", command=inserir_despesa).grid(row=2, column=0, columnspan=2, pady=10)

            root.mainloop()

        Thread(target=run_tk).start()

    def inserir_no_banco(self, tipo, categoria, valor, limite=None, nome=None):         # aqui eu acho melhor nao fazer a função e sim já usar o do arquivo Modify_user_data
        nome = self.db.returnLastLogin()
        if tipo == 'receita':                                                           #   corrigido
            # Cria a tabela 'receita' com as colunas corretas se não existir
            self.db.inserir_receita(nome, valor, limite)
        elif tipo == 'despesa':
            self.db.inserir_despesa(nome, valor, None, categoria, None, False)
