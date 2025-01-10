import sqlite3

import sqlite3
from datetime import datetime


# criar objeto para base de dados
class DataBase:
    def __init__(self):
        self.variable_cost = ['mercado', 'lazer', 'viagem', 'impostos', 'outros']
        self.fixed_cost = ['educação', 'aluguel', 'saúde', 'assinaturas/serviços']
        self.create_table()

    # verifica se tabela 'user' já existe, caso contrário será criada
    def create_table(self):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuario'")
        if not cursor.fetchone():
            cursor.execute("CREATE TABLE  IF NOT EXISTS usuario "
                           "(nome TEXT, sobrenome TEXT, apelido TEXT, senha TEXT)")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='despesa'")
        if not cursor.fetchone():
            cursor.execute('''CREATE TABLE IF NOT EXISTS despesa (
                                nome TEXT NOT NULL, valor REAL NOT NULL, 
                                tipo TEXT NOT NULL, dia TEXT NOT NULL,
                                descricao TEXT)''')

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='receita'")
        if not cursor.fetchone():
            cursor.execute('''CREATE TABLE IF NOT EXISTS receita  (
                               nome TEXT NOT NULL, valor REAL NOT NULL,
                               limite REAL DEFAULT 0, mes TEXT NOT NULL)''')

        database.commit()
        database.close()


    # checar dados de login
    def check_login(self, name, password):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("SELECT * FROM usuario WHERE nome=? AND senha=?", (name, password,))
        usuario = cursor.fetchone()

        if usuario:
            stored_password = usuario[3]
            if stored_password == password:
                database.close()
                return usuario[2]
            database.close()
            return 2
        database.close()
        print("Usuário não encontrado na base de dados.\n")
        return 1

    # insere novo 'user' no banco de dados
    def create_user(self, name, surname, username, password):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("SELECT * FROM usuario WHERE nome = ?", (name,))

        if not cursor.fetchone():
            cursor.execute("INSERT INTO usuario (nome, sobrenome, apelido, senha) "
                           "VALUES (?, ?, ?, ? )",
                           (name, surname, username, password))

            database.commit()
            database.close()
            return 0
        else:
            print("Usuário já cadastrado.\n")

        database.commit()
        database.close()
        return 3

    # apagar histórico de usuário
    def clear_user(self, name):
        database = sqlite3.connect("Data/historic_player.db")
        cursor = database.cursor()

        cursor.execute("DELETE FROM usuario WHERE nome=?",
                       (name,))

        database.commit()
        database.close()

    def return_time(self):
        day, month, year = datetime.now().strftime('%d'), datetime.now().strftime('%m'), datetime.now().strftime('%Y')
        data = day + month + year[2:]

        return data

    def inserir_despesa(self, nome, valor, dia, tipo, descricao, extrato):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        if tipo is None:
            tipo = "Desconhecido"

        if extrato:
            data = dia
        else:
            data = self.return_time()

        payday = '05'

        if extrato:
            data = dia

        if tipo in self.fixed_cost:
            for i in range(2, 6):
                payday += data[i]

        cursor.execute("INSERT INTO despesa (nome, valor, tipo, dia, descricao) "
                       "VALUES (?, ?, ?, ?, ?)",
                       (nome, valor, tipo, data, descricao))

        database.commit()
        database.close()

    def inserir_receita(self, nome, valor, limite):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        data = self.return_time()
        month = data[2:4]

        cursor.execute("SELECT * FROM receita WHERE nome=?", (nome,))

        if cursor.fetchone():
            cursor.execute("INSERT INTO receita (nome, valor, limite, mes)"
                           " VALUES (?, ?, ?, ?)",
                           (nome, valor, limite, month))

        database.commit()
        database.close()

    def modificar_despesa(self, nome, valor, tipo, descricao):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        if tipo is None:
            tipo = "Desconhecido"
        data = self.return_time()

        cursor.execute("SELECT * FROM despesa WHERE nome = ?", (nome,))

        if cursor.fetchone:
            cursor.execute("UPDATE despesa SET valor=?, tipo=?, dia=?, descricao=? WHERE nome=?",
                           (valor, tipo, data, descricao, nome))

        database.commit()
        database.close()

    # incrementa receita ou limite de mês
    def modificar_receita(self, name, valor, limite, mes):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        # incrementa na receita para mês atual e anterior (via extratos bancários)
        if mes:
            month = mes
            cursor.execute("SELECT * FROM receita WHERE nome=? AND mes=?",
                           (name, mes))
            record = cursor.fetchone()

            if record:
                cursor.execute("UPDATE receita SET valor=valor + ? WHERE nome=? AND mes=?",
                               (valor, name, mes))

            # se não houver coluna para o mes inserido, criar-la
            else:
                if limite:
                    cursor.execute("INSERT INTO receita (nome, valor, limite, mes)"
                                   " VALUES (?, ?, ?, ?)",
                                   (valor, name, limite, mes))
                else:
                    cursor.execute("INSERT INTO receita (nome, valor, mes)"
                                   " VALUES (?, ?, ?)",
                                   (name, valor, mes))

        # definir receita para mes atual e os seguintes
        else:
            cursor.execute("SELECT * FROM receita WHERE nome=? ",
                           (name,))
            data = self.return_time()
            month = data[2:4]

            for i in range(11):
                if int(month) < 12:
                    month = int(month) + 1
                    # preencher meses com um elemento nulo para representação de mes
                    if month < 10:
                        month = '0' + str(month)
                    cursor.execute("SELECT * FROM receita WHERE nome = ?",
                                   (name,))

                    record = cursor.fetchone()

                    if record:
                        cursor.execute("UPDATE receita SET valor=?, limite=?, mes=? WHERE nome=?",
                                       (valor, limite, month, name))
                    else:
                        cursor.execute("INSERT INTO receita (nome, valor, limite, mes) VALUES (?, ?, ?, ?)",
                                       (name, valor, limite, month))

        database.commit()
        database.close()

    def remover_despesa(self, nome, valor, dia):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("DELETE FROM despesa WHERE nome=? AND valor=? AND dia=?",
                       (nome, valor, dia))

        database.commit()
        database.close()

    def remover_receita(self, nome, valor, month):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("DELETE FROM receita WHERE nome=? AND valor=? AND mes=?",
                       (nome, valor, month))

        database.commit()
        database.close()

    def retornar_despesas_totais(self, nome):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("SELECT valor FROM despesa WHERE nome=?", (nome,))
        valor = cursor.fetchall()
        cursor.execute("SELECT tipo FROM despesa WHERE nome=?", (nome,))
        tipo = cursor.fetchall()
        cursor.execute("SELECT dia FROM despesa WHERE nome=?", (nome,))
        dia = cursor.fetchall()
        cursor.execute("SELECT descricao FROM despesa WHERE nome=?", (nome,))
        descricao = cursor.fetchall()

        return valor, tipo, dia, descricao

    def retornar_receitas_totais(self, nome):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("SELECT valor FROM receita WHERE nome=?", (nome,))
        valor = cursor.fetchall()
        cursor.execute("SELECT limite FROM receita WHERE nome=?", (nome,))
        limite = cursor.fetchall()
        cursor.execute("SELECT mes FROM receita WHERE nome=?", (nome,))
        mes = cursor.fetchall()

        return valor, limite, mes

    # >>>------------- Funções em teste -------------<<< #

    def print_todas_despesas(self):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("SELECT * FROM despesa")

        todas_as_despesas = cursor.fetchall()

        for despesa in todas_as_despesas:
            print(despesa)

        database.close()

    def print_todas_receitas(self):
        database = sqlite3.connect("Data/info_user.db")
        cursor = database.cursor()

        cursor.execute("SELECT * FROM receita")

        todas_as_receitas = cursor.fetchall()

        for receitas in todas_as_receitas:
            print(receitas)

        database.close()

    def __dell__(self): pass


#  --------------- >>> AMBIENTE DE TESTE <<< ---------------  #

user = DataBase()
user.create_user('Giordano', 'Lanna', 'Giordano', '0123')
# user.check_login('Elisa', '0123')
# check_login('Alfrodo', 1234)



#  --------------- >>> AMBIENTE DE TESTE <<< ---------------  #

# user = DataBase()
# user.create_user('Giordano', 'Lanna', 'Giordano', '0123')
# user.check_login('Elisa', '0123')
# check_login('Alfrodo', 1234)
