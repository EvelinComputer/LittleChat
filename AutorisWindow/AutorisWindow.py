from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow
from Server.Server import LittleChatServer
from DataBase.DataBase import DataBase_MySQL
from ChatWindow.LittleChat import LittleChat
from RegistrWindow.RegistrationAcc import RegistrationAcc

class AutorisWindow(QMainWindow):

    def __init__(self, server : LittleChatServer):

        # Наследуем конструктор QMainWindow
        super(AutorisWindow, self).__init__()

        # Загружаем UI форму (Qt Designer)
        uic.loadUi("./AutorisWindow/AutorisWindow.ui", self)

        # Подключение к серверу
        self.__Server = server

        self.B_Enter.clicked.connect(self.EnterClick)
        self.B_ToReg.clicked.connect(self.ToRegistration)

        self.__registrationWindow = RegistrationAcc(self.__Server)
        self.__registrationWindow.goToAutorisation.connect(self.slotShowWindow)

        self.__chatWindow = LittleChat()
        self.__chatWindow.goToAutorisation.connect(self.slotShowWindow)

    # Установка стиля для текста с сообщением
    def errorLabel(self):
        style_sheet = 'background:  #D0CBDC;\n'\
                        'color: #6E677F;\n'\
                        'border-radius: 20px; '

        return style_sheet

    def ghostLabel(self):
        style_sheet = 'background:  #D0CBDC;\n'\
                        'color: #6E677F;\n'\
                        'border-radius: 20px; '

        return style_sheet

    # Смена окна
    def EnterClick(self):

        # Создание переменных для данных аккаунта
        login = self.LE_Login.text()            # Создаём переменную с логином
        password = self.LE_Password.text()      # Создаём переменную с паролем

        # Проверяем существует ли аккаунт
        state, message = self.__Server.checkAccountDB(login, password)

        # Если существует
        if state:
            self.__chatWindow.showFullScreen()              # Показываем окно чата
            self.hide()                                     # Скрываем окно авторизации
            self.L_Error.setStyleSheet(self.ghostLabel())
            self.L_Error.setText('')                        # Очищаем строку предуприждения об ошибке
            self.LE_Login.setText('')                       # Очищаем строку с логином
            self.LE_Password.setText('')                    # Очищаем строку с паролем

        # Если произошла какая-та ошибка
        else:
            self.L_Error.setStyleSheet(self.errorLabel())
            self.L_Error.setText(message)



    # Переход к окну регистрации
    def ToRegistration(self):
        self.__registrationWindow.showFullScreen()
        self.hide()

    # Показ окна в полноэкранном режиме
    def slotShowWindow(self):
        self.showFullScreen()