import sys

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout


class Example(QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['ID', 'Word', 'Key','TrasFrench','TrasSpanish'])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.lblID = QLabel("Verbs(1) Nouns(2) Adjectives(3) Adverbs(4):")
        self.txtID = QLineEdit()
        self.txtID.setPlaceholderText("Unique Number")

        self.lblWord = QLabel("Word:")
        self.txtWord = QLineEdit()
        self.txtWord.setPlaceholderText("Word")

        self.lblKey = QLabel("Key:")
        self.txtKey = QLineEdit()
        self.txtKey.setPlaceholderText("Meaning")

        self.lblTrasFrench = QLabel("TrasFrench:")
        self.txtTrasFrench = QLineEdit()
        self.txtTrasFrench.setPlaceholderText("Traduction in French")

        self.lblTrasSpanish = QLabel("TrasSpanish:")
        self.txtTrasSpanish = QLineEdit()
        self.txtTrasSpanish.setPlaceholderText("Traduction in Spanish")


        grid = QGridLayout()
        grid.addWidget(self.lblID, 0, 0)
        grid.addWidget(self.txtID, 0, 1)
        grid.addWidget(self.lblWord, 1, 0)
        grid.addWidget(self.txtWord, 1, 1)
        grid.addWidget(self.lblKey, 2, 0)
        grid.addWidget(self.txtKey, 2, 1)
        grid.addWidget(self.lblTrasFrench, 3, 0)
        grid.addWidget(self.txtTrasFrench, 3, 1)
        grid.addWidget(self.lblTrasSpanish, 4, 0)
        grid.addWidget(self.txtTrasSpanish, 4, 1)


        btnCargar = QPushButton('Cargar Datos')
        btnCargar.clicked.connect(self.cargarDatos)

        btnInsertar = QPushButton('Insertar')
        btnInsertar.clicked.connect(self.insertarDatos)

        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(self.eliminarDatos)

        hbx = QHBoxLayout()
        hbx.addWidget(btnCargar)
        hbx.addWidget(btnInsertar)
        hbx.addWidget(btnEliminar)

        vbx = QVBoxLayout()
        vbx.addLayout(grid)
        vbx.addLayout(hbx)
        vbx.setAlignment(Qt.AlignTop)
        vbx.addWidget(self.table)

        self.setWindowTitle("PyQT :: SQLite Data Access")
        self.resize(562, 520)
        self.setLayout(vbx)

    def cargarDatos(self, event):
        index = 0
        query = QSqlQuery()
        query.exec_("select * from person")

        while query.next():
            ids = query.value(0)
            Word = query.value(1)
            Key = query.value(2)
            TrasFrench = query.value(3)
            TrasSpanish = query.value(4)

            self.table.setRowCount(index + 1)
            self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.table.setItem(index, 1, QTableWidgetItem(Word))
            self.table.setItem(index, 2, QTableWidgetItem(Key))
            self.table.setItem(index, 3, QTableWidgetItem(TrasFrench))
            self.table.setItem(index, 4, QTableWidgetItem(TrasSpanish))

            index += 1

    def insertarDatos(self, event):
        ids = int(self.txtID.text())
        Word = self.txtWord.text()
        Key = self.txtKey.text()
        TrasFrench = self.txtTrasFrench.text()
        TrasSpanish = self.txtTrasSpanish.text()


        query = QSqlQuery()
        query.exec_("insert into person values({0}, '{1}', '{2}','{3}','{4}')".format(ids, Word, Key,TrasFrench,TrasSpanish))

    def eliminarDatos(self, event):
        selected = self.table.currentIndex()
        if not selected.isValid() or len(self.table.selectedItems()) < 1:
            return

        ids = self.table.selectedItems()[0]
        query = QSqlQuery()
        query.exec_("delete from person where id = " + ids.text())

        self.table.removeRow(selected.row())
        self.table.setCurrentIndex(QModelIndex())

    def db_connect(self, filename, server):
        db = QSqlDatabase.addDatabase(server)
        db.setDatabaseName(filename)
        if not db.open():
            QMessageBox.critical(None, "Cannot open database",
                    "Unable to establish a database connection.\n"
                    "This example needs SQLite support. Please read the Qt SQL "
                    "driver documentation for information how to build it.\n\n"
                    "Click Cancel to exit.", QMessageBox.Cancel)
            return False
        return True

    def db_create(self):
        query = QSqlQuery()
        query.exec_("create table person(id int primary key, "
                    "firstname varchar(20), lastname varchar(20))")
        query.exec_("insert into person values(1, 'Walk', 'to ','Young','Marche')")
      
    def init(self, filename, server):
        import os
        if not os.path.exists(filename):
            self.db_connect(filename, server)
            self.db_create()
        else:
            self.db_connect(filename, server)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ejm = Example()
    ejm.init('datafile', 'QSQLITE')
    ejm.show()
    sys.exit(app.exec_())

