import logging as log


# Создание класса для аккаунтов
class Account:
    # Создание локальных переменных
    __id = int
    __login = str
    __password = str
    __pincode = str

    def __init__(self, id, login, password, pincode):
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
        if str(type(account)) == "<class 'DataBase.Account'>":  # Проверка на тип данных аккаунта
            for elem in self:  # Проверка на ID
                if elem.getID() == account.getID():
                    log.error('Аккаунт с таким ID уже существует')
                    return None
            self.append(account)
        else:
            log.error('Неверный тип данных для аккаунта')

    # Нахождение аккаунта по ID
    def getByID(self, id):
        for item in self:
            if item.getID() == id:
                return item

        log.error("Такого аккаунта нет")
        return None

    # Нахождение аккаунта по логину
    def getByLogin(self, login):
        for item in self:
            if item.getLogin() == login:
                return item.getID()

    # Удаление аккаунта по ID
    def removeAccountByID(self, id):
        for num in range(len(self)):
            if self[num].getID() == id:
                return self.pop(num)
        log.error("Такого аккаунта нет")
        return None


