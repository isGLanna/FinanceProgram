import tkinter
import re
from abc import ABC, abstractmethod
from datetime import datetime
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from CreateUserDatabase import DataBase


# PARA GERAR PDF É NECESSÁRIO CRIAR UMA CLASSE " PdfFile " e rodar o método " write_document "
class DocumentWriter(ABC):
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def write(self):
        pass

    def mm2p(self, mm):
        return mm/0.35


# inserir dados financeiros
class PdfWriter(DocumentWriter):
    def __init__(self, filename, data, descrition, expense):
        super().__init__(filename)
        self.__data = data
        self.__descrition = descrition
        self.__expense = expense

    def mm2p(self, mm):
        return mm/0.35

    def write(self):
        doc = self.filename

        doc.setFont('Helvetica', 11)    # data da despesa
        px, py = 15, 255
        for data in self.__data:
            data = re.sub(r'\D', '', data[0])

            data = data[:2] + '/' + data[2:4] + '/20' + data[4:]
            doc.drawString(self.mm2p(px), self.mm2p(py), str(data))
            py -= 6

            if py < 15:
                break

            # descrição
        doc.setFont('Helvetica', 10)
        px, py = 41, 255
        for descrition in self.__descrition:
            descrition = descrition[0]

            if not descrition:
                descrition = '-- Sem informação de pagamento --'
            descrition = descrition.replace("(", "").replace(")", "").replace(",", "")
            doc.drawString(self.mm2p(px), self.mm2p(py), descrition[:80])
            py -= 6
            if py < 15:
                break

            # despesas
        doc.setFont('Helvetica', 11)
        px, py = 180, 255
        for expense in self.__expense:
            if '-' in str(expense[0]):
                expense = str(expense[0])
            else:
                expense = '-' + str(expense[0])
            expense = expense.replace("(", "").replace(")", "").replace(",", "")
            doc.drawString(self.mm2p(px), self.mm2p(py), str(expense))
            py -= 6
            if py < 15:
                break


# inserir informações visuais/extras
class PdfDesigner(DocumentWriter):
    def __init__(self, filename, name, revenue):
        super().__init__(filename)
        self.name = name
        self.text = 'CLIENTE - ' + self.name
        self.__revenue = revenue
        self.__total_revenue = 0.0

    def mm2p(self, mm):
        return mm/0.35

    def complete_data(self):
        day, month, year = datetime.now().strftime('%d'), datetime.now().strftime('%m'), datetime.now().strftime(
            '%Y')
        hours = datetime.now().strftime('%H')+':' + datetime.now().strftime('%M')+':'+datetime.now().strftime('%S')
        data = day + '/' + month + '/' + year
        return data, hours

    # desenhar linhas
    def drawLines(self):
        doc = self.filename
        doc.line(40, 745, 570, 745)
        doc.line(40, 820, 570, 820)
        doc.line(275, 775, 570, 775)
        doc.line(275, 820, 275, 745)
        doc.line(570, 820, 570, 25)
        doc.line(40, 820, 40, 25)
        doc.line(40, 25, 570, 25)

    def write(self):
        doc = self.filename
        data, hours = self.complete_data()

        text_data = 'Data de geração:'
        text_revenue = 'Receitas:'

        self.drawLines()

        # data de geração do documento
        px, py = 100, 280
        doc.setFont('Helvetica', 13)
        doc.drawString(self.mm2p(px), self.mm2p(py), text_data)

        px, py = 155, 280
        doc.setFont('Helvetica', 14)
        doc.drawString(self.mm2p(px), self.mm2p(py), data)

        px, py = 155, 274
        doc.setFont('Helvetica', 12)
        doc.drawString(self.mm2p(px), self.mm2p(py), '   ' + hours)

        # informações gerais
        px, py = 20, 272
        doc.setFont('Helvetica', 20)
        doc.drawString(self.mm2p(px), self.mm2p(py), self.text)

        # receitas totais
        for value in self.__revenue:
            self.__total_revenue += value[0]
        self.__total_revenue = round(self.__total_revenue, 2)

        px, py = 100, 265
        doc.setFont('Helvetica', 13)
        doc.drawString(self.mm2p(px), self.mm2p(py), text_revenue)

        px, py = 155, 265
        doc.setFont('Helvetica', 14)
        doc.drawString(self.mm2p(px), self.mm2p(py), 'R$ ' + str(self.__total_revenue))


class PdfFile:
    def __init__(self, nome):
        self.filename = None
        self.__nome = nome

        self.__expense = []
        self.__data = []
        self.__descrition = []

        self.__revenue = []
        self.__month = []

        self.bd = DataBase()

        self.save_pdf()

    def save_pdf(self):
        root = tkinter.Tk()
        root.withdraw()

        self.filename = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            filetypes=[('PDF files', '*.pdf')],
            title="Salvar arquivo PDF",
        )
        self.write_document()

    def write_document(self):
        self.getExpense()
        self.getRevenue()
        doc = canvas.Canvas(self.filename, pagesize=A4)

        pdf = PdfWriter(doc,  self.__data, self.__descrition, self.__expense)
        pdf_designer = PdfDesigner(doc, self.__nome, self.__revenue)
        pdf.write()
        pdf_designer.write()

        doc.save()

    def getExpense(self):
        self.__expense, trash, self.__data, self.__descrition = self.bd.retornar_despesas_totais(self.__nome)

    def getRevenue(self):
        self.__revenue, trash, self.__month = self.bd.retornar_receitas_totais(self.__nome)


#  --------------- >>> AMBIENTE DE TESTE <<< ---------------  #

test = PdfFile('Giordano')
test.write_document()
