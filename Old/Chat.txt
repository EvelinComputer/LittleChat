import logging as log
from DataBase.Account import Account

# Создание класса для списка ID аккаунтов, которые могут пользоваться чатом
class IdAccounts(list):
    # Очистка списка
    def clear(self):
        self.clear()

    # Добавление ID
    def addId(self, account):
        if type(account) == type(Account()):
            id = account.getID()  # Получение id аккаунта
            # Проверка на присутствие этого ID в чате
            for elem in self:  # Перебор списка ID аккаунтов
                if id in self:  # Проверка на присутствие этого ID
                    log.error('Этот аккаунт уже существует в этом чате')  # Выдача ошибки
                    return None
            self.append(id)  # Добавление
        else:
            log.error('Неверный тип данных для аккаунта')  # Выдача ошибки

    # Удаление ID
    def removeId(self, id):
        if id in self:  # Перебор списка ID аккаунтов
            self.remove(id)  # Удаление ID
            return None
        else:
            log.error('Этого ID нету в этом чате')  # Выдача ошибки

    # Выдача списка ID
    def getIdAccounts(self):
        return self


# Создание класса для одного чата
class Chat:
    # Создание локальных переменных
    __id = int                  # ID чата
    __name = str                # Наименования чата
    __idAccounts = IdAccounts   # Список ID аккаунтов, которые могут пользоваться чатом

    # Конструктор лего
    def __init__(self, id, name):
        # С этими переменными вроде всё ок
        self.__id = id                    # ID чата
        self.__name = name                # Наименования чата
        self.__idAccounts = IdAccounts()  # Список ID аккаунтов, которые могут пользоваться чатом

    # Установка ID
    def setID(self, id):
        self.__id = id

    # Выдача ID
    def getID(self):
        return self.__id

    # Установка наименования чата
    def setName(self, name):
        self.__name = name

    # Выдача наименования чата
    def getName(self):
        return self.__name

    # Установка списка ID аккаунтов
    def setIdAccounts(self, new):
        self.__idAccounts = new

    # Выдача списка ID аккаунтов
    def getIdAccounts(self):
        return self.__idAccounts

    def __str__(self):
        return "ID: {0}\nName: {1}\nID Accounts: {2}".format(self.__id, self.__name, self.__idAccounts)


# Создание класса для базы данных чатов (основная основа так сказать, если не считать предыдущий класс)
class ChatList(list):

    # Добавление чата
    def addChat(self, chat):
        if str(type(chat)) == "<class 'DataBase.Chat.Chat'>":
            for elem in self:  # Проверка на ID
                if elem.getID() == chat.getID():
                    log.error('Чат с таким ID уже существует')  # Выдача ошибки
                    return None
            self.append(chat)  # Добавление чата
        else:
            log.error('Неверный тип данных для чата')  # Выдача ошибки

    # Нахождение чата по ID
    def getByID(self, id):
        for elem in self:  # Перебор элементов в списке чатов
            if elem.getID() == id:  # Проверка на ID
                return elem

        log.error("Такого чата нет")  # Выдача ошибки
        return None

    # Нахождение чата по наименованию
    def getByName(self, name):
        for elem in self:  # Перебор элементов в списке чатов
            if elem.getName() == name:  # Проверка на наименование
                return elem.getID()

    # Удаление чата по ID
    def removeAccountByID(self, id):
        for num in range(len(self)):  # Перебор индексов элементов в списке чатов
            if self[num].getID() == id:  # Проверка на ID
                return self.pop(num)
        log.error("Такого чата нет")  # Выдача ошибки
        return None

