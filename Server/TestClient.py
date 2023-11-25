import datetime
import logging as log
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QTcpSocket, QHostAddress, QHostInfo, QAbstractSocket


class LittleChatClient(QObject):

    def __init__(self):

        super(LittleChatClient, self).__init__()

        log.basicConfig()
        self.__logger = log.getLogger()
        self.__logger.setLevel(log.INFO)

        self.__Client__ = QTcpSocket()
        self.__Client__.connected.connect(self.__connectedToComplete)
        self.__Client__.stateChanged.connect(self.__stateChanged)
        self.__Client__.readyRead.connect(self.__reader)

        self.__Client__.connectToHost(QHostAddress('127.0.0.1'), 1010)
        self.__logMessage('>>> Start client "Little Chat" <<<')

    def __connectedToComplete(self):
        self.__logMessage("Подключение установлено!")

    def __stateChanged(self, state):
        self.__logMessage(str(state))
        if state == QAbstractSocket.SocketState.ConnectedState:
            self.__Client__.write(str.encode(str("Hello")))

    def __reader(self):
        message = str(self.__Client__.readAll(), 'utf-8')
        if message[:2] == 'M|':
            self.__logMessage(message[2:])
        elif message[:2] == 'E|':
            self.__logError(message[2:])
        elif message[:3] == 'CA|':
            self.__logMessage("Autorisation account...")
        else:
            self.__logMessage("TCP: " + message)
        command = str(input('>>> '))
        self.__Client__.write(str.encode(command))

    def __logMessage(self, message: str):
        self.__logger.info(" " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " | " + message)

    def __logError(self, message: str):
        self.__logger.error(" " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " | " + message)

    def checkAcc(self, login, password):
        command = f"CA|{login}|{password}"  # CA - Check Account (Проверить аккаунт)
        self.__Client__.write(str.encode(command))


def Main():
    # Запуск QT ядра
    App = QApplication([])

    Client = LittleChatClient()

    # Запуск
    App.exec()


if __name__ == "__main__": Main()
