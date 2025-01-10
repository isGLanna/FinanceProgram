import tkinter as tk
from tkinter import messagebox
import sqlite3
from CreateAccountApp import CreateAccountApp
from DisplayManager import DisplayManager


def check_login(user, password):
    database = sqlite3.connect("Data/info_user.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM usuario WHERE nome=?", (user,))
    usuario = cursor.fetchone()

    if usuario:
        stored_password = usuario[3]        # Supondo que a senha está na quarta coluna
        if stored_password == password:
            nome = usuario[0]               # Supondo que o nome está na primeira coluna
            sobrenome = usuario[1]          # Supondo que o sobrenome está na segunda coluna
            database.close()
            return nome, sobrenome          # Retorna o nome e sobrenome
    database.close()
    return None, None                       # Retorna None se o login falhar


class LoginApp:
    def __init__(self, root, name=None, surname=None):
        self.create_conta = None
        self.root = root
        self.root.title("Tela de Login")
        self.login_successful = False
        self.name = None
        self.surname = None

        self.center_window(550, 320)        # Centralizar janela

        self.frame = tk.Frame(root,
                              bg="black",
                              bd=0.5,
                              relief="solid")
        self.frame.pack(pady=5,
                        padx=10,
                        fill="both",
                        expand=True)

        self.label_user = tk.Label(self.frame,
                                   text="Usuário",
                                   fg="white",
                                   bg="black",
                                   font=("Segoe UI", 16))
        self.label_user.pack(pady=(10, 5))

        self.entry_user = tk.Entry(self.frame,
                                   fg="black",
                                   bg="green",
                                   font=("Segoe UI", 16),
                                   width=30)
        self.entry_user.pack()

        self.label_password = tk.Label(self.frame,              # Label e Entry de Senha dentro do Frame
                                       text="Senha",
                                       fg="white",
                                       bg="black",
                                       font=("Segoe UI", 16))
        self.label_password.pack(pady=(10, 5))

        self.entry_password = tk.Entry(self.frame,
                                       show="*",
                                       fg="black",
                                       bg="green",
                                       font=("Segoe UI", 16),
                                       width=30)
        self.entry_password.pack()

        self.login_button = tk.Button(self.frame,               # Botão de Login dentro do Frame
                                      text="Login",
                                      command=self.login,
                                      bg="gray",
                                      fg="black",
                                      font=("Segoe UI", 16))
        self.login_button.pack(pady=(10, 5))

        self.create_account_button = tk.Button(self.frame,      # Botão de Criar Conta dentro do Frame
                                               text="Criar Conta",
                                               command=self.create_account,
                                               bg="gray",
                                               fg="black",
                                               font=("Segoe UI", 16))
        self.create_account_button.pack(pady=(10, 5))

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')


    def login(self):
        try:
            user = self.entry_user.get()
            password = self.entry_password.get()

            if len(password) > 20:                              # Verifica se a senha tem mais de 20 caracteres
                raise ValueError("A senha não pode ter mais que 20 caracteres.")

            nome, sobrenome = check_login(user, password)       # Verifica login e obtém nome e sobrenome do usuário
            if nome and sobrenome:
                self.name = nome
                self.surname = sobrenome
                self.login_successful = True
                self.root.destroy()                             # Fecha a janela de login
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos")
        except ValueError as ve:
            messagebox.showerror("Erro", str(ve))           # Mostra a mensagem de erro para o usuário
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")  # Caso precise tratar outros erros inesperados
        finally:
            print("Tentativa de login finalizada.")

    def create_account(self):
        self.create_conta = CreateAccountApp(self.root)

    '''def start_main_interface(self):
        display_manager = DisplayManager(self.name, self.surname)
        display_manager.draw_interface()'''
