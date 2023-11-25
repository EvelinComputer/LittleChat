from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal


class RegistrationWindow(QMainWindow):

    # Сигнал на возвращение в окно авторизации
    sigShowAutoris = pyqtSignal()
    sigLogError = pyqtSignal(str)
    sigLogMessage = pyqtSignal(str)

    def __init__(self):
        super(RegistrationWindow, self).__init__()                       # Наследуем конструктор QMainWindow
        uic.loadUi("./RegistrWindow/Registration.ui", self)     # Загружаем UI форму (Qt Designer)

        self.B_Registration.clicked.connect(self.__RegistrationClick)
        self.B_ToSignUp.clicked.connect(self.__ToEnter)
        self.B_Exit.clicked.connect(self.hide)
        self.B_Close.clicked.connect(self.showMinimized)

    def __RegistrationClick(self):
        # Создание аккаунта и дальнейшая регистрация
        login = self.LE_Login.text()                    # Создаём логин
        password = self.LE_Password.text()              # Создаём пароль
        pincode = self.LE_Pincode.text()                # Создаём пинкод
        lastName = self.LE_LastName.text()              # Создаём фамилию
        firstName = self.LE_FirstName.text()            # Создаём имя
        phoneNumber = self.LE_PhoneNumber.text()        # Создаём номер телефона
        email = self.LE_Email.text()                    # Создаём почту

        """ @TODO заменить сервер на клиент """
        state, message = None, None #self.__Server.newAccountDB(login=login,
                                    #                           password=password,
                                    #                           last_name=lastName,
                                    #                           first_name=firstName,
                                    #                           phone_number=phoneNumber,
                                    #                           email=email,
                                    #                           pincode=pincode)

        if state:
            self.ToEnter()
            # Очищение строк
            self.LE_Login.setText('')
            self.LE_Password.setText('')
            self.LE_Pincode.setText('')
            self.LE_LastName.setText('')
            self.LE_FirstName.setText('')
            self.LE_PhoneNumber.setText('')
            self.LE_Email.setText('')
        else:
            self.L_Error.setText(message)

    # Переход к окну авторизации
    def __ToEnter(self):
        self.hide()                         # Закрытие окна
        self.sigShowAutoris.emit()
