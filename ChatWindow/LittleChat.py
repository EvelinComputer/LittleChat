from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal
from Server.Server import LittleChatServer


class LittleChat(QMainWindow):
    goToAutorisation = pyqtSignal()

    def __init__(self):
        super(LittleChat, self).__init__()                       # Наследуем конструктор QMainWindow
        uic.loadUi("./ChatWindow/Window.ui", self)         # Загружаем UI форму (Qt Designer)

        self.B_First.clicked.connect(self.button_clicked)
        self.B_Push.clicked.connect(self.button_push)

    # Переход в окно регистрация (ну или выйти из аккаунта)
    def button_clicked(self):
        self.hide()
        self.goToAutorisation.emit()

    # Нажатие кнопки отправки сообщений
    def button_push(self):
        text_message = self.TE_Message.toPlainText()
        self.LW_Chat.addItem(text_message)
        self.TE_Message.setText('')

