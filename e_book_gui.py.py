import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QGridLayout, QLineEdit)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import (QFont, QIcon)
import e_book_def_einlesen
import e_book_def_auswertung



class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        QToolTip.setFont(QFont('Calibri', 10))

        grid = QGridLayout()
        self.setLayout(grid)
        
        self.setToolTip('Auswertungstool für das Statistische E-Book.')
        
        self.ent_name = QLineEdit('Rohdaten.xlsx', self)
        self.ent_name.setToolTip('Name der Datei, die ausgewertet werden soll (Excel-Datei)')
        grid.addWidget(self.ent_name, *[2,2])   

        self.ent_name2 = QLineEdit('DAX', self)
        self.ent_name2.setToolTip('Name des Wetes, der ausgewertet werden soll')
        grid.addWidget(self.ent_name2, *[3,2])   

        self.rohdaten = None
        btw = QPushButton('Einlesen', self)
        btw.setToolTip('Einlesen der Rohdaten.')
        btw.clicked.connect(lambda: self.einlesen())
        grid.addWidget(btw, *[4,2])

        btver = QPushButton('Grund_Verarbeitung', self)
        btver.setToolTip('Verarbeiten der Daten.')
        btver.clicked.connect(lambda: e_book_def_auswertung.aus_grund(self.rohdaten, self.ent_name2.text()))
        grid.addWidget(btver, *[5,2])

        bttest = QPushButton('Test', self)
        bttest.setToolTip('Zum testen des Programms.')
        bttest.clicked.connect(lambda: e_book_def_auswertung.excel_export(self.rohdaten, self.ent_name2.text()))
        grid.addWidget(bttest, *[6,2])     
        btq = QPushButton('Quit', self)
        btq.setToolTip('Beendet das Programm!')
        btq.clicked.connect(QCoreApplication.instance().quit)
        grid.addWidget(btq, *[7,2])   

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('E-Book')
        self.setWindowIcon(QIcon('tesla_icon.png'))        
    
        self.show()

    def einlesen(self):
        self.rohdaten = e_book_def_einlesen.daten_einlesen(self.ent_name.text())

    def onChanged(self, text):
        print(self.name_dat)        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
