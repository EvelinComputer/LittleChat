import logging as log


# Создание класса для аккаунтов
class Account:

    # Создание локальных переменных
    __id = int  # ID аккаунта
    __login = str  # Логин аккаунта
    __password = str  # Пароль аккаунта
    __pincode = str  # Пинкод аккаунта

    def __init__(self, id = None, login = None, password = None, pincode = None):
        self.__id = id
        self.__login = login
        self.__password = password
        self.__pincode = pincode

    # Установка ID
    def setID(self, id):
        self.__id = id

    # Выдача ID
    def getID(self):
        return self.__id

    # Установка логина
    def setLogin(self, login):
        self.__login = login

    # Выдача логина
    def getLogin(self):
        return self.__login

    # Установка пароля
    def setPassword(self, password):
        self.__password = password

    # Выдача пароля
    def getPassword(self):
        return self.__password

    # Установка пинкода
    def setPincode(self, pincode):
        self.__pincode = pincode

    # Выдача пинкода
    def getPincode(self):
        return self.__pincode

    def __str__(self):
        return "ID: {0}\nLogin: {1}\nPassword: {2}\nPincode: {3}".format(self.__id, self.__login, self.__password,
                                                                         self.__pincode)


# Создание класса для списка аккаунтов или базы данных
class AccountList(list):
    # Добавление аккаунта
    def addAccount(self, account):
        if type(account) == type(Account()):  # Проверка на тип данных аккаунта
            for elem in self:  # Проверка на ID
                if elem.getID() == account.getID():  # Проверка на идентичность ID
                    log.error('Аккаунт с таким ID уже существует')  # Выдача ошибки
                    return None
            self.append(account)  # Добавление аккаунта

        else:
            log.error('Неверный тип данных для аккаунта')  # Выдача ошибки

    # Нахождение аккаунта по ID
    def getByID(self, id):
        for item in self:  # Перебор списка аккаунтов
            if item.getID() == id:  # Проверка на верность ID
                return item

        log.error("Такого аккаунта нет")  # Выдача ошибки
        return None

    # Нахождение аккаунта по логину
    def getByLogin(self, login):
        for item in self:  # Перебор списка аккаунтов
            if item.getLogin() == login:  # Проверка на верность логина
                return item.getID()

        log.error("Такого аккаунта нет")  # Выдача ошибки
        return None

    # Удаление аккаунта по ID
    def removeAccountByID(self, id):
        for num in range(len(self)):  # Перебор индексов списка аккаунтов
            if self[num].getID() == id:  # Проверка на верность id
                return self.pop(num)

        log.error("Такого аккаунта нет")  # Выдача ошибки
        return None


