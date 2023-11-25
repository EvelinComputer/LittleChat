import sys
import datetime
import logging as log

from PyQt6 import uic
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtNetwork import QTcpServer, QHostAddress, QHostInfo, QTcpSocket, QAbstractSocket

sys.path.append("./../DataBase")
from DataBase import DataBase_MySQL

'''@TODO ГДЕ КОММЕНТАРИИ !!!'''
class ClientList(list):

    def __init__(self):
        super(ClientList, self).__init__()
        self.__IDS__ = []                       # Список ID
        self.__Logins__ = []                    # Список логинов
        self.__CounterClients__ = 0             # Счётчик клиентов

    # Добавление клиента
    def addClient(self, client):
        # Проверка на тип данных
        if type(client) == type(QTcpSocket()):
            # Добавление клиента во всевозможные списки
            self.append(client)
            self.__IDS__.append(self.__CounterClients__)
            self.__Logins__.append('Ghost')
            self.__CounterClients__ += 1
            return self.__CounterClients__ - 1
        return -1

    # Установка логина по ID
    def setLoginByID(self, id, login):
        self.__Logins__[id] = login

    # Выдача логина по ID
    def getLoginByID(self, id):
        return self.__Logins__[id]

    # Выдача ID по клиенту
    def getID(self, client):
        return self.index(client)

    # Выдача индекса по ID в списке с ID
    def getByID(self, id):
        index = self.__IDS__.index(id)
        if index >= 0:
            return self[index]
        return None

'''@TODO ГДЕ КОММЕНТАРИИ !!!'''
class LittleChatServer(QMainWindow):

    def __init__(self):

        super(LittleChatServer, self).__init__()
        uic.loadUi("server.ui", self)

        # Магия над log
        log.basicConfig()
        self.__logger = log.getLogger()
        self.__logger.setLevel(log.INFO)

        self.__Power = False

        # Подключение к базе данных
        self.__DB = DataBase_MySQL()
        if self.__DB.isConnected():
            self.__logMessage(">>> Connected to MySQL")
        else:
            self.__logError(">>> Not connected to MySQL")

        # Создание локальных переменных, связанных с сервером
        self.__ClientAdmin__ = QTcpSocket()
        self.__ClientAdmin__.stateChanged.connect(self.__stateChangedClient)
        self.__Server__ = QTcpServer()
        self.__Server__.newConnection.connect(self.__newConnection)
        self.__ClientList__ = ClientList()

        # Обработка кнопки
        self.B_Push.clicked.connect(self.__PushClicked)
        self.B_Clear.clicked.connect(self.__ClearClicked)

        # Запуск сервера
        self.__CMD_Start()

    # Старт
    def __CMD_Start(self, ip='127.0.0.1', port=1010):

        self.__IP__ = QHostAddress(str(ip))
        self.__Port__ = int(port)

        if self.__DB.isConnected():
            if self.__Server__.listen(self.__IP__, self.__Port__):
                self.__logMessage('>>> Start server "Little Chat"')
                self.__logMessage('>>> Address: {0}:{1}'.format(self.__IP__.toString(), self.__Port__))
                self.__ClientAdmin__.connectToHost(self.__IP__, self.__Port__)
                self.__Power = True
            # Ошибка при старте
            else:
                self.__logError('Error start server')
        else:
            self.__logError('Error start server')

    # Проверка аккаунта (функция для базы данных)
    def checkAccountDB(self, login, password):
        return self.__DB.checkAccount(login, password)

    # Создание аккаунта (функция для базы данных)
    def newAccountDB(self, login, password, last_name, first_name, phone_number, email, pincode):
        return self.__DB.newAccount(login, password, last_name, first_name, phone_number, email, pincode)

    def __PushClicked(self):
        text = self.LE_Command.text()
        self.LE_Command.setText("")
        if self.__Power and text[0] != '/':
            self.__ClientAdmin__.write(str.encode(str(text)))
        else:
            if(text == "/StartMySQL"):
                if(self.__DB.isConnected()):
                    self.__logError(">>> MySQL already working")
                else:
                    if self.__DB.reconnect():
                        self.__logMessage(">>> Connected to MySQL")
                    else:
                        self.__logError(">>> Not connected to MySQL")
            elif text == "/StartServer":
                if self.__Power:
                    self.__logError(">>> Server already working")
                else:
                    self.__CMD_Start()

    def __ClearClicked(self):
        self.LW_Console.clear()




    # Функция, которая вызывается при подключении нового клиента
    def __newConnection(self):

        # Новый клиент
        newClient = self.__Server__.nextPendingConnection()
        if(len(self.__ClientList__) > 0): self.__logMessage('>>> Connect new client')

        # ID и связка функций клиента
        id = self.__ClientList__.addClient(newClient)
        self.__ClientList__.getByID(id).disconnected.connect(self.__disconnectedClient)
        self.__ClientList__.getByID(id).readyRead.connect(self.__readyReadClient)

        # Проверка на админа (админ ВСЕГДА с 0 ID)
        if id == 0:
            self.__ClientList__.setLoginByID(id, 'ADMIN')

    # def __connectedClient(self):
    #    self.__logMessage('Connect')

    # Функция, которая вызывается при отключении клиента
    def __disconnectedClient(self):
        # Информация о клиенте
        client = self.sender()
        id = self.__ClientList__.getID(client)
        login = self.__ClientList__.getLoginByID(id)

        # Сообщение о отключении клиента
        self.__logMessage('ID: {0} -> User: "{1}" is disconnected'.format(id, login))

    # Функция, которачя вызывается при изменении состояния у админа
    def __stateChangedClient(self, state):
        self.__logMessage('Admin State: ' + str(state))

        # Условие, которое срабатывает, когда админ подключается к серверу
        if state == QAbstractSocket.SocketState.ConnectedState:
            self.__ClientAdmin__.write(str.encode("<IsAdmin>"))

    # Функция, которая вызывается при обработке команд
    def __readyReadClient(self):
        # Информация о клиенте (сам клиент, ID и его команда)
        client = self.sender()
        id = self.__ClientList__.getID(client)
        command = str(self.__ClientList__.getByID(id).readAll(), 'utf-8')
        self.__logMessage('ID: {0} -> User: "{1}" -> Command: "{2}"'.
                          format(str(id), self.__ClientList__.getLoginByID(id), command))

        # Обработка команд
        keyError = True
        message = "Command not found!"

        # ----
        if command == '<Check>':
            keyError = False
            message = 'YOU "{0}"'.format(self.__ClientList__.getLoginByID(id))

        # ---
        elif command == '<IsAdmin>':
            if id == 0:
                message = 'YOU ADMIN'
                self.__logMessage(message)
                return
            else:
                keyError = True
                message = 'Not permission'
                # <CA>|a|a|</>

        # Обработка команды Check Account
        elif command.find("<CA>") == 0:

            # Расшифровка пакета
            tmp = command.split('|')
            login = str(tmp[1])
            password = str(tmp[2])

            # Проверка акккаунта на существование
            keyError, result = self.__DB.checkAccount(login, password)

            # Отправка клиенту сообщения об авторизации
            client.write(str.encode("<CA>|" + str(keyError) + "|" + result + "|</>"))

            keyError = not keyError

            # Если ошибка
            if(keyError):
                message = "Ошибка авторизации!"

            # Если авторизация пройдена
            else:
                message = result

                # Получение имени аккаунта
                data = self.__DB.getNameAccount(login)
                client.write(str.encode("<NAME>|" + str(data[0]) + "|" + str(data[1]) + "|</>"))


        if keyError:
            client.write(str.encode("<E>|" + message + "|</>"))
            self.__logError('ID: {0} -> User: "{1}" -> Error: "{2}"'.
                            format(str(id), self.__ClientList__.getLoginByID(id), message))
        else:
            client.write(str.encode("<M>|" + message + "|</>"))
            self.__logMessage('ID: {0} -> User: "{1}" -> Push: "{2}"'.
                              format(str(id), self.__ClientList__.getLoginByID(id), message))

    # Функции для упрощения работы с log
    def __logMessage(self, message: str):
        text = datetime.datetime.utcnow().isoformat(sep=' ', timespec='milliseconds') + " | " + message
        self.__logger.info(" " + text)
        self.LW_Console.addItem(text)

    def __logError(self, message: str):
        text = datetime.datetime.utcnow().isoformat(sep=' ', timespec='milliseconds') + " | " + message
        self.__logger.error(" " + text)
        self.LW_Console.addItem(text)


def Main():
    # Запуск QT ядра
    App = QApplication([])

    Server = LittleChatServer()
    Server.show()

    # Запуск
    App.exec()


if __name__ == "__main__": Main()
