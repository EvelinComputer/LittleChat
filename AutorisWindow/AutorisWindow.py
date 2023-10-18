from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, QTimer
from DataBase import Account
from RegistrWindow.RegistrationAcc import RegistrationAcc
from ChatWindow.LittleChat import LittleChat

class AutorisWindow(QMainWindow):
    def __init__(self, base):
        super(AutorisWindow, self).__init__()  # Наследуем конструктор QMainWindow
        uic.loadUi("./AutorisWindow/AutorisWindow.ui", self)  # Загружаем UI форму (Qt Designer)

        self.DataBase = base  # База данных

        self.B_Enter.clicked.connect(self.EnterClick)
        self.B_ToReg.clicked.connect(self.ToRegistration)

        self.__registrationWindow = RegistrationAcc(self.DataBase)
        self.__registrationWindow.goToAutorisation.connect(self.slotShowWindow)

        self.__chatWindow = LittleChat()
        self.__chatWindow.goToAutorisation.connect(self.slotShowWindow)

    # Установка стиля для текста с сообщением
    def errorLabel(self):
        style_sheet = 'background: rgb(255, 212, 111);\n'\
                        'color: rgb(74, 61, 21);\n'\
                        'border-radius: 17px; '

        return style_sheet

    # Смена окна
    def EnterClick(self):
        # Создание переменных для данных аккаунта
        login = self.LE_Login.text()  # Создаём переменную с логином
        self.LE_Login.setText('')  # Очищаем строку с логином
        password = self.LE_Password.text()  # Создаём переменную с паролем
        self.LE_Password.setText('')  # Очищаем строку с паролем

        id = self.DataBase.getAccountIDbyLogin(login)  # Создаём переменную с ID

        # Проверка на верность введённых данных
        if id >= 0:
            tmp = self.DataBase.getAccount(id)  # Переменная с аккаунтом
            if tmp.getPassword() == password:  # Проверка на верность пароля
                # Выдача сообщения об успешной авторизации
                self.L_Error.setStyleSheet(self.errorLabel())
                self.L_Error.setText('Авторизация проведена')
                print('Авторизация проведена')  # Авторизация проведена
                # Переход к окну чата
                self.hide()
                self.__chatWindow.show()
            else:
                # Выдача ошибки
                self.L_Error.setStyleSheet(self.errorLabel())
                self.L_Error.setText('Пароль неверный')
                print('Error. Пароль неправильный')
        else:
            # Выдача ошибки
            self.L_Error.setStyleSheet(self.errorLabel())
            self.L_Error.setText('Логин не найден')
            print('Error. Логин не найден')

    # Переход к окну регистрации
    def ToRegistration(self):
        self.hide()
        self.__registrationWindow.show()

    # Показ окна
    def slotShowWindow(self):
        self.show()