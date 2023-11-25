from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QMainWindow

class AutorisWindow(QMainWindow):

    sigShowReg = pyqtSignal()
    sigShowChat = pyqtSignal()
    sigLogError = pyqtSignal(str)
    sigLogMessage = pyqtSignal(str)
    sigCheckAccount = pyqtSignal(str, str)

    def __init__(self):

        # Наследуем конструктор QMainWindow
        super(AutorisWindow, self).__init__()

        # Загружаем UI форму (Qt Designer)
        uic.loadUi("./AutorisWindow/AutorisWindow.ui", self)

        self.B_Enter.clicked.connect(self.__EnterClick)
        self.B_ToReg.clicked.connect(self.__ToRegistration)
        self.B_Exit.clicked.connect(self.hide)
        self.B_Close.clicked.connect(self.showMinimized)

    # Установка стиля для текста с сообщением
    def __errorLabel(self):
        style_sheet = 'background:  #D0CBDC;\n'\
                        'color: #6E677F;\n'\
                        'border-radius: 20px; '

        return style_sheet

    def __ghostLabel(self):
        style_sheet = 'background:  #D0CBDC;\n'\
                        'color: #6E677F;\n'\
                        'border-radius: 20px; '

        return style_sheet

    # Смена окна
    def __EnterClick(self):

        # Создание переменных для данных аккаунта
        login = self.LE_Login.text()            # Создаём переменную с логином
        password = self.LE_Password.text()      # Создаём переменную с паролем

        self.sigCheckAccount.emit(login, password)


        """ @TODO заменить сервер на клиент """
        # Проверяем существует ли аккаунт
        #state, message = self.__Client.checkAcc(login, password)


        # Если существует
        '''if state:
            self.sigShowChat.emit()              # Показываем окно чата
            self.hide()                                     # Скрываем окно авторизации
            self.L_Error.setStyleSheet(self.__ghostLabel())
            self.L_Error.setText('')                        # Очищаем строку предуприждения об ошибке
            self.LE_Login.setText('')                       # Очищаем строку с логином
            self.LE_Password.setText('')                    # Очищаем строку с паролем

        # Если произошла какая-та ошибка
        else:
            self.L_Error.setStyleSheet(self.__errorLabel())
            self.L_Error.setText(message)'''


    # Переход к окну регистрации
    def __ToRegistration(self):
        self.sigShowReg.emit()
        self.hide()

    # Показ окна в полноэкранном режиме
    def slotShowWindow(self):
        self.showFullScreen()
