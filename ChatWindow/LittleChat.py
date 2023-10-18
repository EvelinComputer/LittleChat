from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal


class LittleChat(QMainWindow):
    goToAutorisation = pyqtSignal()

    def __init__(self):
        super(LittleChat, self).__init__()      # Наследуем конструктор QMainWindow
        uic.loadUi("./ChatWindow/Window.ui", self)         # Загружаем UI форму (Qt Designer)

        self.B_First.clicked.connect(self.button_clicked)

    # Переход в окно регистрация (ну или выйти из аккаунта)
    def button_clicked(self):
        self.hide()
        self.goToAutorisation.emit()




        # 0%    = 200
        # n%    = 300
        # 100%  = 400
        # h = (Max - Min / 100) = (400 - 200) / 100 = 2
        # n = (Val - Min) / h = 300 - 200 / 2 = 100/2 = 50