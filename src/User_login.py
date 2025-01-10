import sqlite3
from datetime import datetime





# retorna data atual e próximos meses



# >>>------------- Funções de teste -------------<<< #

def print_todas_despesas():
    database = sqlite3.connect("Data/info_user.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM despesa")

    todas_as_despesas = cursor.fetchall()

    for despesa in todas_as_despesas:
        print(despesa)

    database.close()


def print_todas_receitas():
    database = sqlite3.connect("Data/info_user.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM receita")

    todas_as_receitas = cursor.fetchall()

    for receitas in todas_as_receitas:
        print(receitas)

    database.close()


#  --------------- >>> AMBIENTE DE TESTE <<< ---------------  #

# modificar_receita('Giordano', 500, 1000, None)
# print_todas_receitas()
# inserir_despesa('Giordano', 500.00, '030821', 'aluguel', "Palmeira não tem mundial", True)
# inserir_despesa(1234, 30.00, 'aposta')
# inserir_despesa(1234, 58.00, 'alimento')
# print_todas_despesas()
