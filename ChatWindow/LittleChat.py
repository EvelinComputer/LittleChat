from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal

class LittleChat(QMainWindow):
    goToAutorisation = pyqtSignal()

    def __init__(self):
        super(LittleChat, self).__init__()      # Наследуем конструктор QMainWindow
        uic.loadUi("./ChatWindow/Window.ui", self)         # Загружаем UI форму (Qt Designer)

        print(self.T_Chatik.text())
        self.T_Chatik.setText('Надпись')
        self.LCD.display(222)
        self.Progress.setRange(0, 100)
        self.Progress.setValue(65)
        self.Progress.setFormat("Идёт загрузка...")

        self.B_First.clicked.connect(self.button_clicked)
        self.B_Second.clicked.connect(self.button_second_clicked)

        self.R_First.toggled.connect(lambda:self.radio_button_react(self.R_First))
        self.R_Second.toggled.connect(lambda:self.radio_button_react(self.R_Second))

        self.C_Check.setCheckState(Qt.CheckState.PartiallyChecked)
        self.C_Check.stateChanged.connect(self.galochka)

    def button_clicked(self):
        self.hide()
        self.goToAutorisation.emit()

    def button_second_clicked(self):
        print(self.E_lineChat.text())
        self.E_lineChat.setText('')

    def radio_button_react(self, RButton):
        print(RButton.text())

    def galochka(self, arg__2):
        print(arg__2)




        # 0%    = 200
        # n%    = 300
        # 100%  = 400
        # h = (Max - Min / 100) = (400 - 200) / 100 = 2
        # n = (Val - Min) / h = 300 - 200 / 2 = 100/2 = 50