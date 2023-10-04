from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
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

    def EnterClick(self):
        # Создание переменных для данных аккаунта
        ''' login = self.LE_Login.text()  # Создаём переменную с логином
        self.LE_Login.setText('')  # Очищаем строку с логином
        password = self.LE_Password.text()  # Создаём переменную с паролем
        self.LE_Password.setText('')  # Очищаем строку с паролем

        id = self.DataBase.getIDbyLogin(login)  # Создаём переменную с ID

        # Проверка на верность введённых данных
        if id >= 0:
            tmp = self.DataBase.getAccount(id)  # Переменная с аккаунтом
            if tmp.getPassword() == password:  # Проверка на верность пароля
                print('Авторизация проведена')
            else:
                print('Error. Пароль неправильный')
        else:
            print('Error. Логин не найден') '''
        self.hide()
        self.__chatWindow.show()

    # Вообще эта функция должна переносить в другое окно, нооо она этого не делает (пока)
    def ToRegistration(self):
        self.hide()
        self.__registrationWindow.show()

    def slotShowWindow(self):
        self.show()
