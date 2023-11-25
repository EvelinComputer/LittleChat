from PyQt6.QtNetwork import QTcpSocket, QHostAddress, QHostInfo, QAbstractSocket
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QMessageBox

from AutorisWindow import AutorisWindow as AW
from ChatWindow import ChatWindow as CW
from Server.TestClient import LittleChatClient
from RegistrWindow import RegistrationWindow as RW
import logging as log
import datetime


class LittleChat(QObject):

    # Сигнал сообщеает об успешной авторизации
    sigSuccessAutoris = pyqtSignal()

    def __init__(self):
        # Наследуем конструктор QMainWindow
        super(LittleChat, self).__init__()

        # Система логирования
        log.basicConfig()
        self.__logger = log.getLogger()
        self.__logger.setLevel(log.INFO)

        # Глобавльные переменные
        self.__successAutorisation = False        # Состояние авторизации
        self.__messageAutorisation = ""           # Сообщение авторизации
        self.__answerAutorisation = False         # Ответ состояния авторизации
        self.__firstName = ""                     # Имя клиента
        self.__lastName = ""                      # Фамилия клиента

        self.__Timer = QTimer()                   # Таймер общего значения
        self.__timerCount = 0                     # Счётчик для таймера

        # Создание окон
        self.__AutorisWin = AW.AutorisWindow()
        self.__ChatWin = CW.ChatWindow()
        self.__RegistrWin = RW.RegistrationWindow()

        # Установка системы логирования
        self.__AutorisWin.sigLogMessage.connect(self.__logMessage)
        self.__AutorisWin.sigLogError.connect(self.__logError)
        self.__ChatWin.sigLogMessage.connect(self.__logMessage)
        self.__ChatWin.sigLogError.connect(self.__logError)
        self.__RegistrWin.sigLogMessage.connect(self.__logMessage)
        self.__RegistrWin.sigLogError.connect(self.__logError)

        # Соединение сигналов
        self.__AutorisWin.sigCheckAccount.connect(self.__CheckAccount)
        self.__AutorisWin.sigShowChat.connect(self.__ShowChat)
        self.__AutorisWin.sigShowReg.connect(self.__ShowReg)
        self.__RegistrWin.sigShowAutoris.connect(self.__ShowAutoris)
        self.__ChatWin.sigShowAutoris.connect(self.__ShowAutoris)

        self.__Timer.timeout.connect(self.__Timeout)

        # Настройка сетевого подключения
        self.__Client__ = QTcpSocket()
        self.__Client__.stateChanged.connect(self.__ClientStateChanged)
        self.__Client__.disconnected.connect(self.__ClientDisconnected)
        self.__Client__.connected.connect(self.__ClientConnected)
        self.__Client__.errorOccurred.connect(self.__ClientError)
        self.__Client__.hostFound.connect(self.__ClientHostFound)
        self.__Client__.readyRead.connect(self.__Reader)

        # Запуск клиента
        self.__logMessage('>>> Start client "Little Chat" <<<')
        self.__Client__.connectToHost(QHostAddress('127.0.0.1'), 1010)

    def __logMessage(self, message: str):
        self.__logger.info(" " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " | " + message)

    def __logError(self, message: str):
        self.__logger.error(" " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " | " + message)

    # Запуск программы
    def start(self):
        self.__ShowAutoris()

    # Показ окна регистрации
    def __ShowReg(self):
        self.__RegistrWin.showFullScreen()

    # Показ окна авторизации
    def __ShowAutoris(self):
        self.__AutorisWin.showFullScreen()

    # Показ окна чата
    def __ShowChat(self):
        self.__ChatWin.showFullScreen()

    def __ClientConnected(self):
        self.__logMessage("Connect to server")

    def __ClientStateChanged(self, state):
        self.__logMessage("State: " + str(state))
        if state == QAbstractSocket.SocketState.ConnectedState:
            self.__Client__.write(str.encode(str("<Check>")))

    def __ClientDisconnected(self):
        self.__logMessage("Disconnect to server")

    def __ClientError(self, error):
        self.__logError("Error: " + str(error))

    def __ClientHostFound(self):
        self.__logMessage("Server found")

    def __CheckAccount(self, login: str, password: str):
        self.__Client__.write(str.encode("<CA>|{0}|{1}|</>".format(login, password)))
        self.__timerCount = 0
        self.__Timer.start(200)

    def __Timeout(self):
        self.__timerCount += 1

        if self.__answerAutorisation:
            if self.__successAutorisation:
                if self.__firstName != "" and self.__lastName != "":
                    self.__ChatWin.showFullScreen()
                    self.__AutorisWin.hide()
                    self.__Timer.stop()
                    self.__timerCount = 0
                    self.__answerAutorisation = False
                    return None
            else:
                QMessageBox.warning(None, "Авторизация", self.__messageAutorisation)
                self.__Timer.stop()
                self.__timerCount = 0
                self.__answerAutorisation = False
                return None

        # Когда время вышло
        if self.__timerCount == 10:
            self.__Timer.stop()
            self.__timerCount = 0
            QMessageBox.critical(None, "Ошибка", "Превышен интервал лимита ожидания.")

    # Обработка команд от сервера
    def __Reader(self):

        # Получение команд
        command = str(self.__Client__.readAll(), 'utf-8')

        # Создание списка команд от сервера
        command_arr = command.split("</>")

        # Последовательное выполнение команд от сервера
        for id in range(len(command_arr) - 1):

            # Получение нужной команды
            command = command_arr[id]

            # Обработка команды Message (M)
            if command.find("<M>") == 0:
                self.__logMessage("Server: " + command.split("|")[1])

            # Обработка команды Error (E)
            elif command.find("<E>") == 0:
                self.__logError("Server: " + command.split("|")[1])

            # Обработка команды Check Account (CA)
            elif command.find("<CA>") == 0:
                self.__messageAutorisation = str(command.split('|')[2])
                if command.split('|')[1] == "True":
                    self.__successAutorisation = True
                else:
                    self.__successAutorisation = False
                self.__answerAutorisation = True

            # Обработка команды Name (NAME)
            elif command.find("<NAME>") == 0:
                self.__lastName = command.split('|')[1]
                self.__firstName = command.split('|')[2]
                self.__logMessage("Имя: '{0}' Фамилия: '{1}'".format(self.__firstName, self.__lastName))


            # Если команда неизвестна
            else:
                self.__logMessage("TCP: " + command)

