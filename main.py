from PyQt5 import uic
from PyQt5.QtWidgets import *
import sqlite3
import sys


PRODUCT_ID = ''
EDIT_ROW = False

class ClssDialog(QDialog):
    def __init__(self, parent=None):
        super(ClssDialog, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.sql()

        self.setupUi(self)
        self.pushButton_save.clicked.connect(
            self.save)  # Сохранить данные
        self.pushButton_save.clicked.connect(
            self.submitclose)  # Сохранить данные

    def sql(self):
        global PRODUCT_ID, ADD_ROW
        if EDIT_ROW:
            con = sqlite3.connect("coffee.db")
            cur = con.cursor()
            print(PRODUCT_ID)
            text_sql = f'SELECT * FROM price  WHERE  id = {PRODUCT_ID}'
            result = list(cur.execute(text_sql).fetchone())
            self.label_ID.setText(str(result[0]))
            self.lineEditName.setText(str(result[1]))
            self.lineEditStepen.setText(str(result[2]))
            self.lineEditTip.setText(str(result[3]))
            self.lineEditOpisanie.setText(str(result[4]))
            self.lineEditCena.setText(str(result[5]))
            self.lineEditObem.setText(str(result[6]))


    def setupUi(self, MainWindow):
        pass
        # sets up Submit button

    def submitclose(self):
        self.accept()

    def save(self):
        con = sqlite3.connect("coffee.db")
        cur = con.cursor()
        if EDIT_ROW:
            con = sqlite3.connect("coffee.db")
            cur = con.cursor()
            id = self.label_ID.text()
            name = self.lineEditName.text()
            stepen = self.lineEditStepen.text()
            tip = self.lineEditTip.text()
            opisanie = self.lineEditOpisanie.text()
            cena = self.lineEditCena.text()
            obem = self.lineEditObem.text()
            text_sql = f' UPDATE price SET Name = ?, Stepen = ?, Tip = ?, ' \
                       f' Opisanie = ?,  Cena = ?,  Obem = ?  WHERE id = ?'
            task = [name, stepen, tip, opisanie, cena, obem, id]
            cur.execute(text_sql, task)
        else:
            con = sqlite3.connect("coffee.db")
            cur = con.cursor()
            name = self.lineEditName.text()
            stepen = self.lineEditStepen.text()
            tip = self.lineEditTip.text()
            opisanie = self.lineEditOpisanie.text()
            cena = self.lineEditCena.text()
            obem = self.lineEditObem.text()
            text_sql = f'INSERT INTO price(Name, Stepen, Tip, Opisanie,' \
                       f' Cena, Obem) VALUES(?,?,?,?,?,?)'

            task = [name, stepen, tip, opisanie, cena, obem]
            cur.execute(text_sql, task)
        con.commit()
        con.close()
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.fill()

        self.pushButton.clicked.connect(self.fill)
        self.pushButton_add.clicked.connect(
            self.open_dialog)  # Открыть новую форму для добавления
        self.pushButton_edit.clicked.connect(
            self.edit_row)  # Открыть новую форму для редактирования


    def fill(self):
        self.tableWidget.clear()
        self.del_row()

        labels = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
                  'Описание вкуса', 'Цена', 'Объем упаковки']
        self.test6 = labels
        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(labels)
        with sqlite3.connect("coffee.db") as connect:
            for ID, Name, Stepen, Tip, Opisanie, Cena, Obem in connect.execute(
                    """SELECT * FROM price where ID > 0"""):
                row = self.tableWidget.rowCount()
                self.tableWidget.setRowCount(row + 1)
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(ID)))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(Name))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(Stepen))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(Tip))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(Opisanie))
                self.tableWidget.setItem(row, 5, QTableWidgetItem(str(Cena)))
                self.tableWidget.setItem(row, 6, QTableWidgetItem(str(Obem)))

        self.tableWidget.resizeColumnsToContents()

    def del_row(self):
        for d in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)

    def edit_row(self):
        global PRODUCT_ID, EDIT_ROW
        EDIT_ROW = True
        PRODUCT_ID = (self.tableWidget.item(self.tableWidget.currentRow(),
                                            0).text())
        print(f'select_row = {PRODUCT_ID}')
        if PRODUCT_ID != -1:
            self.w = ClssDialog()
            if self.w.exec_():
                print(PRODUCT_ID)
                self.fill()

    def open_dialog(self):
        global EDIT_ROW
        EDIT_ROW = False
        self.w = ClssDialog()
        if self.w.exec_():
            self.fill()


app = QApplication(sys.argv)
ui = MainWindow()
ui.show()
sys.exit(app.exec_())
