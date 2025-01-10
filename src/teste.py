import sqlite3

def updateLastLogin(nome):
    conn = sqlite3.connect('Data/info.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS last_login (nome TEXT)")

    cursor.execute("SELECT COUNT(*) FROM last_login")
    count = cursor.fetchone()[0]

    if count > 0:
        cursor.execute("UPDATE last_login SET nome = ?", (nome,))
    else:
        cursor.execute("INSERT INTO last_login (nome) VALUES (?)", (nome,))

    conn.commit()
    conn.close()


def returnLasLogin():
    conn = sqlite3.connect('Data/info.db')
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM last_login")
    nome = cursor.fetchone()

    conn.close()
    return nome[0]

updateLastLogin('Testando')
name = returnLasLogin()
print(name)
