import tkinter as tk
from tkinter import messagebox
from CreateUserDatabase import DataBase


class CreateAccountApp:
    def __init__(self, root, login_app=None):
        self.login_app = login_app
        self.root = root
        self.root.title("Criar Conta")
        self.user_name = None
        self.user_surname = None

        # Centraliza a janela
        self.center_window(550, 720)

        self.frame = tk.Frame(root,
                              bg="black",
                              bd=0.5,
                              relief="solid")
        self.frame.pack(pady=5,
                        padx=10,
                        fill="both",
                        expand=True)

        # Label e Entry de Nome de usuário dentro do Frame
        self.label_username = tk.Label(self.frame,
                                       text="Nome de usuário:",
                                       fg="white",
                                       bg="black",
                                       font=("Segoe UI", 16))
        self.label_username.pack(pady=(10, 5))

        self.entry_username = tk.Entry(self.frame,
                                       fg="black",
                                       bg="green",
                                       font=("Segoe UI", 16),
                                       width=30)
        self.entry_username.pack(pady=5)

        # Label e Entry de Senha dentro do Frame
        self.label_password = tk.Label(self.frame,
                                       text="Senha:",
                                       fg="white",
                                       bg="black",
                                       font=("Segoe UI", 16))
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(self.frame,
                                       show="*",
                                       fg="black",
                                       bg="green",
                                       font=("Segoe UI", 16),
                                       width=30)
        self.entry_password.pack(pady=5)

        # Label e Entry de Nome dentro do Frame
        self.label_name = tk.Label(self.frame,
                                   text="Nome:",
                                   fg="white",
                                   bg="black",
                                   font=("Segoe UI", 16))
        self.label_name.pack(pady=5)

        self.entry_name = tk.Entry(self.frame,
                                   fg="black",
                                   bg="green",
                                   font=("Segoe UI", 16),
                                   width=30)
        self.entry_name.pack(pady=5)

        # Label e Entry de Sobrenome dentro do Frame
        self.label_surname = tk.Label(self.frame,
                                      text="Sobrenome:",
                                      fg="white",
                                      bg="black",
                                      font=("Segoe UI", 16))
        self.label_surname.pack(pady=5)

        self.entry_surname = tk.Entry(self.frame,
                                      fg="black",
                                      bg="green",
                                      font=("Segoe UI", 16),
                                      width=30)
        self.entry_surname.pack(pady=5)

        # Botão de Criar Conta dentro do Frame
        self.button_create = tk.Button(self.frame,
                                       text="Criar Conta",
                                       command=self.create_account,
                                       bg="gray",
                                       fg="black",
                                       font=("Segoe UI", 16))
        self.button_create.pack(pady=20)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_account(self):
        db = DataBase()
        username = self.entry_username.get()
        password = self.entry_password.get()
        name = self.entry_name.get()
        surname = self.entry_surname.get()

        result = db.create_user(name, surname, username, password)

        if result == 0:
            messagebox.showinfo("Conta criada", "Conta criada com sucesso!")
            self.user_name = name
            self.user_surname = surname
            self.root.destroy()  # Fecha a janela de criação de conta

            if self.login_app:
                self.login_app.user_name = name
                self.login_app.user_surname = surname
                self.root.destroy()

            # Reabre a tela de login
            login_root = tk.Tk()
            from LoginApp import LoginApp
            LoginApp(login_root, name = self.user_name, surname = self.user_surname)
            login_root.mainloop()

        elif result == 3:
            messagebox.showerror("Erro", "Usuário já cadastrado.")
