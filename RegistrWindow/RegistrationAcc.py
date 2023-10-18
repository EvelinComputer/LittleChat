from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal
from DataBase.Account import Account


class RegistrationAcc(QMainWindow):

    # Сигнал на возвращение в окно авторизации
    goToAutorisation = pyqtSignal()

    def __init__(self, base):
        super(RegistrationAcc, self).__init__()  # Наследуем конструктор QMainWindow
        uic.loadUi("./RegistrWindow/Registration.ui", self)  # Загружаем UI форму (Qt Designer)
        self.DataBase = base  # Создаём или загружаем базу данных

        self.B_Registration.clicked.connect(self.RegistrationClick)
        self.B_ToSignUp.clicked.connect(self.ToEnter)

    def RegistrationClick(self):
        # Создание аккаунта и дальнейшая регистрация
        login = self.LE_Login.text()  # Создаём логин
        self.LE_Login.setText('')  # Очищаем строку
        password = self.LE_Password.text()  # Создаём пароль
        self.LE_Password.setText('') # Очищаем строку x2
        pincode = self.LE_Pincode.text()  # Создаём пинкод
        self.LE_Pincode.setText('')  # Мне надоело писать "очищаем строку"

        acc = Account(id=self.DataBase.lenAccounts(), login=login, password=password, pincode=pincode)  # Создание аккаунта
        self.DataBase.addAccount(acc)  # Добавляем аккаунт
        self.DataBase.save("DataBase.db")
        print(login, password, pincode)  # Выводим данные от аккаунта в консоль

    # Переход к окну авторизации
    def ToEnter(self):
        self.hide()  # Закрытие окна
        self.goToAutorisation.emit()