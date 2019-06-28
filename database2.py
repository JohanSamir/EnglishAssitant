import sys

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout


class Example(QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(['ID', 'Type', 'Word', 'Key','TrasFrench','TrasSpanish'])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setColumnWidth(3,550)

        self.lblID = QLabel("ID:")
        self.txtID = QLineEdit()
        self.txtID.setPlaceholderText("Number:")

        self.lblIDType = QLabel("Type:")
        self.txtIDType = QLineEdit()
        self.txtIDType.setPlaceholderText("Verbs(1) Nouns(2) Adjectives(3) Adverbs(4):")

        self.lblName = QLabel("Word:")
        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText("Word")

        self.lblApellido = QLabel("Key")
        self.txtApellido = QLineEdit()
        self.txtApellido.setPlaceholderText("Meaning")

        self.lblApellido2 = QLabel("TrasFrench:")
        self.txtApellido2 = QLineEdit()
        self.txtApellido2.setPlaceholderText("Traduction in French")

        self.lblApellido3 = QLabel("TrasSpanish:")
        self.txtApellido3 = QLineEdit()
        self.txtApellido3.setPlaceholderText("Traduction in Spanish")

        grid = QGridLayout()
        grid.addWidget(self.lblID, 0, 0)
        grid.addWidget(self.txtID, 0, 1)
        grid.addWidget(self.lblIDType, 1, 0)
        grid.addWidget(self.txtIDType, 1, 1)
        grid.addWidget(self.lblName, 2, 0)
        grid.addWidget(self.txtName, 2, 1)
        grid.addWidget(self.lblApellido, 3, 0)
        grid.addWidget(self.txtApellido, 3, 1)
        grid.addWidget(self.lblApellido2, 4, 0)
        grid.addWidget(self.txtApellido2, 4, 1)
        grid.addWidget(self.lblApellido3, 5, 0)
        grid.addWidget(self.txtApellido3, 5, 1)


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

        self.setWindowTitle("JSOC: Dictionary")
        self.resize(1100, 520)
        self.setLayout(vbx)

    def cargarDatos(self, event):
        index = 0
        query = QSqlQuery()
        query.exec_("select * from person")

        while query.next():
            ids = query.value(0)
            typewo = query.value(1)
            nombre = query.value(2)
            apellido = query.value(3)
            apellido2 = query.value(4)
            apellido3 = query.value(5)

            self.table.setRowCount(index + 1)
            self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.table.setItem(index, 1, QTableWidgetItem(typewo))
            self.table.setItem(index, 2, QTableWidgetItem(nombre))
            self.table.setItem(index, 3, QTableWidgetItem(apellido))
            self.table.setItem(index, 4, QTableWidgetItem(apellido2))
            self.table.setItem(index, 5, QTableWidgetItem(apellido3))


            index += 1

    def insertarDatos(self, event):
        ids = int(self.txtID.text())
        typewo = self.txtIDType.text()
        nombre = self.txtName.text()
        apellido = self.txtApellido.text()
        apellido2 = self.txtApellido2.text()
        apellido3 = self.txtApellido3.text()

        query = QSqlQuery()
        query.exec_("insert into person values({0},'{1}','{2}','{3}','{4}','{5}')".format(ids,typewo,nombre, apellido,apellido2,apellido3))

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
                    "firstname varchar(20), lastname varchar(20), stname varchar(20),sstname varchar(20),ssstname varchar(20))")        
        #query.exec_("insert into person values(102, 'Danny', 'Young')")
        query.exec_("insert into person values(1,'V','Walk','to move along by putting one foot in front of the other','Marche','Caminar')")
        

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

