from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from DataBase import Account


""" Вот такая штука умеет делать воба! """
class Registration(QMainWindow):
    def __init__(self, base):
        super(Registration, self).__init__()  # Наследуем конструктор QMainWindow
        uic.loadUi("./RegistrationEnter.ui", self)  # Загружаем UI форму (Qt Designer)

        self.DataBase = base  # Создаём или загружаем базу данных

        self.B_Reg.clicked.connect(self.RegistrationClick)  # Регистрация аккаунта
        self.B_Enter.clicked.connect(self.EnterClick)  # Вход в аккаунт

    def RegistrationClick(self):
        # Создание аккаунта и дальнейшая регистрация
        login = self.LE_RegLogin.text()  # Создаём логин
        self.LE_RegLogin.setText('')
        password = self.LE_RegPassword.text()  # Создаём пароль
        self.LE_RegPassword.setText('')
        pincode = self.LE_Card.text()  # Создаём пинкод
        self.LE_Card.setText('')
        # acc.registration(login, password, pincode)  # Регистрация

        acc = Account(id=self.DataBase.len(), login=login, password=password, pincode=pincode)  # Создание аккаунта
        self.DataBase.addAccount(acc)  # Добавляем аккаунт

    def EnterClick(self):
        # Вход в аккаунт
        login = self.LE_EnterLogin.text()
        self.LE_EnterLogin.setText('')
        password = self.LE_EnterPassword.text()
        self.LE_EnterPassword.setText('')

        id = self.DataBase.getIDbyLogin(login)

        # Проверка на правильные данные
        if id >= 0:
            tmp = self.DataBase.getAccount(id)
            if tmp.getPassword() == password:
                print('Авторизация проведена')
            else:
                print('Error. Пароль неправильный')
        else:
            print('Error. Логин не найден')
