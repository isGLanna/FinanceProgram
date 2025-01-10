import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import sqlite3

class SistemaFinancas:
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar_banco(self):
        return sqlite3.connect(self.db_path)

    def buscar_despesas(self):
        with self.conectar_banco() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tipo, SUM(valor) FROM despesa GROUP BY tipo")
            despesas = cursor.fetchall()
        return despesas

    def buscar_receitas(self):
        with self.conectar_banco() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT mes, SUM(valor) FROM receita GROUP BY mes")
            receitas = cursor.fetchall()
        return receitas

    def mostrar_grafico_pizza(self):
        despesas = self.buscar_despesas()
        if not despesas:
            messagebox.showinfo("Aviso", "Nenhuma despesa para exibir.")
            return

        categorias = [despesa[0] for despesa in despesas]
        valores = [despesa[1] for despesa in despesas]

        plt.figure(figsize=(8, 6))
        plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140)
        plt.title("Distribuição das Despesas")
        plt.show()

    def mostrar_grafico_receitas(self):
        receitas = self.buscar_receitas()
        if not receitas:
            messagebox.showinfo("Aviso", "Nenhuma receita para exibir.")
            return

        meses = [receita[0] for receita in receitas]
        valores = [receita[1] for receita in receitas]

        plt.figure(figsize=(8, 6))
        plt.bar(meses, valores)
        plt.title("Receitas por Mês")
        plt.xlabel("Mês")
        plt.ylabel("Valor")
        plt.show()

class SistemaFinancasApp:
    def __init__(self, root):
        self.sistema = SistemaFinancas("Data/info_user.db")
        self.root = root
        self.root.title("Sistema de Finanças")

        # Botões
        self.btn_mostrar_grafico_despesas = tk.Button(root, text="Mostrar Gráfico de Despesas", command=self.sistema.mostrar_grafico_pizza)
        self.btn_mostrar_grafico_despesas.grid(row=0, column=0, padx=10, pady=10)

        self.btn_mostrar_grafico_receitas = tk.Button(root, text="Mostrar Gráfico de Receitas", command=self.sistema.mostrar_grafico_receitas)
        self.btn_mostrar_grafico_receitas.grid(row=1, column=0, padx=10, pady=10)


    #   aqui tem que ajeitar para colocar no app.py, no caso quandoo alguém clicar em gerar gráfico
def main():
    root = tk.Tk()
    app = SistemaFinancasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
