import sys

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout


class Example(QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'NOMBRE', 'APELLIDO', 'APELLIDO2'])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.lblID = QLabel("ID:")
        self.txtID = QLineEdit()
        self.txtID.setPlaceholderText("Numero identificador unico")

        self.lblName = QLabel("Nombre:")
        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText("Nombre de la persona")

        self.lblApellido = QLabel("Apellido:")
        self.txtApellido = QLineEdit()
        self.txtApellido.setPlaceholderText("Apellido de la persona")

        self.lblApellido2 = QLabel("Apellido:")
        self.txtApellido2 = QLineEdit()
        self.txtApellido2.setPlaceholderText("Apellido de la persona")

        grid = QGridLayout()
        grid.addWidget(self.lblID, 0, 0)
        grid.addWidget(self.txtID, 0, 1)
        grid.addWidget(self.lblName, 1, 0)
        grid.addWidget(self.txtName, 1, 1)
        grid.addWidget(self.lblApellido, 2, 0)
        grid.addWidget(self.txtApellido, 2, 1)
        grid.addWidget(self.lblApellido2, 3, 0)
        grid.addWidget(self.txtApellido2, 3, 1)

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
            nombre = query.value(1)
            apellido = query.value(2)
            apellido2 = query.value(3)

            self.table.setRowCount(index + 1)
            self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.table.setItem(index, 1, QTableWidgetItem(nombre))
            self.table.setItem(index, 2, QTableWidgetItem(apellido))
            self.table.setItem(index, 3, QTableWidgetItem(apellido2))


            index += 1

    def insertarDatos(self, event):
        ids = int(self.txtID.text())
        nombre = self.txtName.text()
        apellido = self.txtApellido.text()
        apellido2 = self.txtApellido2.text()

        query = QSqlQuery()
        query.exec_("insert into person values({0}, '{1}', '{2}','{3}')".format(ids, nombre, apellido,apellido2))

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
                    "firstname varchar(20), lastname varchar(20), stname varchar(20))")        
        query.exec_("insert into person values(101, 'Danny', 'Young')")
        query.exec_("insert into person values(102, 'Christine', 'Holand','jaja')")
        

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
