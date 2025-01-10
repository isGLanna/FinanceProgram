import pandas
import tkinter
import shutil
import os
from CreateUserDatabase import *
from tkinter import filedialog


class ImportArchives:
    def __init__(self, format, name):
        self.format = format
        self.name = name
        self.file_location = None
        self.bd = DataBase()

        self.open_file(format)

    def open_file(self, format):
        root = tkinter.Tk()
        root.withdraw()
        filetypes = [(f"{format.upper()} files", f"*.{format}")]

        self.file_location = filedialog.askopenfilename(
            title="Importar arquivo",
            filetypes=filetypes,
            defaultextension=".{}".format(format)
        )

    def import_csv(self):
        if self.file_location:
            df = pandas.read_csv(self.file_location)

            data = df['Data'].tolist()
            valor = df['Valor'].tolist()
            descricao = df['Descrição'].tolist()

            for i in range(len(valor)):
                if valor[i] <= 0.0:
                    dia = data[i]
                    dia = dia.replace('/', '')
                    dia = dia[:4] + dia[6:]
                    self.bd.inserir_despesa(self.name, valor[i], dia, None, descricao[i], True)
                else:
                    dia = data[i]
                    dia = dia.replace('/', '')
                    dia = dia[:4] + dia[6:]
                    mes = dia[2:5]
                    self.bd.modificar_receita(self.name, valor[i], None, mes)

    def import_image(self):
        destination = "Data/profile picture/user_{}.png".format(self.name)

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(self.file_location, destination)


#  --------------- >>> AMBIENTE DE TESTE <<< ---------------  #

teste = ImportArchives('csv', "Giordano")
teste.import_csv()
