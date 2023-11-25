from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal


class ChatWindow(QMainWindow):

    sigShowAutoris = pyqtSignal()
    sigLogError = pyqtSignal(str)
    sigLogMessage = pyqtSignal(str)

    def __init__(self):
        super(ChatWindow, self).__init__()                       # Наследуем конструктор QMainWindow
        uic.loadUi("./ChatWindow/Window.ui", self)         # Загружаем UI форму (Qt Designer)

        self.B_First.clicked.connect(self.__button_clicked)
        self.B_Push.clicked.connect(self.__button_push)
        self.B_Exit.clicked.connect(self.hide)
        self.B_Close.clicked.connect(self.showMinimized)

    # Переход в окно регистрация (ну или выйти из аккаунта)
    def __button_clicked(self):
        self.sigShowAutoris.emit()
        self.hide()

    # Нажатие кнопки отправки сообщений
    def __button_push(self):
        text_message = self.TE_Message.toPlainText()
        self.LW_Chat.addItem(text_message)
        self.TE_Message.setText('')


