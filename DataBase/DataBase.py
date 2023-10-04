import logging as log
import json as js
from DataBase.Chat import Chat, ChatList, IdAccounts
from DataBase.Account import Account, AccountList

# Создание полноценной базы данных
class DataBase:
    __BD_Accounts = AccountList()  # Это просто список аккаунтов
    __BD_Chats = ChatList()  # А это список чатов
    # Вроде всё понятно, а дальше начинается резня. Я предупредила!

    def __init__(self):
        self.clear()

    # Очищение базы данных
    def clear(self):
        self.__BD_Accounts.clear()
        self.__BD_Chats.clear()

    # Выдача базы данных
    def getAccountList(self):
        return self.__BD_Accounts

    # Добавление аккаунта в базу данных
    def addAccount(self, account):
        self.__BD_Accounts.addAccount(account)

    # Выдача аккаунта из базы данных по ID
    def getAccount(self, id):
        Acc = self.__BD_Accounts.getByID(id)
        if Acc != None:
            return Acc

    # Удаление аккаунта из базы данных по ID
    def removeAccount(self, id):
        self.__BD_Accounts.removeAccountByID(id)

    # Установка логина для аккаунта по ID
    def setAccountLogin(self, id, login):
        Acc = self.__BD_Accounts.getByID(id)
        if Acc != None:
            return Acc.setLogin(login)

    # Выдача логина аккаунта по ID
    def getAccountLogin(self, id):
        Acc = self.__BD_Accounts.getByID(id)
        if Acc != None:
            return Acc.getLogin()

    # Установка пароля для аккаунта по ID
    def setAccountPassword(self, id, password):
        Acc = self.__BD_Accounts.getByID(id)
        if Acc != None:
            return Acc.setPassword(password)

    # Выдача пароля аккаунта по ID
    def getAccountPassword(self, id):
        Acc = self.__BD_Accounts.getByID(id)
        if Acc != None:
            return Acc.getPassword()

    # Установка пинкода для аккаунта по ID
    def setAccountPincode(self, id, pincode):
        Acc = self.__BD_Accounts.getByID(id)
        if Acc != None:
            return Acc.setPincode(pincode)

    # Выдача пинкода аккаунта по ID
    def getAccountPincode(self, id):
        Acc = self.__BD_Accounts.getByID(id)
        if Acc != None:
            return Acc.getPincode()

    # Выдача ID по логину аккаунта
    def getAccountIDbyLogin(self, login):
        return self.__BD_Accounts.getByLogin(login)

    # Выдача длины списка аккаунтов
    def lenAccounts(self):
        return len(self.__BD_Accounts) + 1

    # Выдача длины списка чатов
    def lenChats(self):
        return len(self.__BD_Chats) + 1

    # Выдача базы данных
    def getChatList(self):
        return self.__BD_Chats

    # Добавление чата в базу данных
    def addChat(self, chat):
        self.__BD_Chats.addChat(chat)

    # Выдача чата из базы данных по ID
    def getChat(self, id):
        chat = self.__BD_Chats.getByID(id)
        if chat != None:
            return chat

    # Удаление чата из базы данных по ID
    def removeChat(self, id):
        self.__BD_Chats.removeAccountByID(id)

    # Установка наименования чата
    def setChatName(self, id, name):
        chat = self.__BD_Chats.getByID(id)
        if chat != None:
            chat.setName(name)

    # Выдача наименования чата по ID
    def getChatName(self, id):
        chat = self.__BD_Chats.getByID(id)
        if chat != None:
            return chat.getName()

    # Установка списка ID аккаунтов по ID
    def setChatIDAccounts(self, id, idAcc):
        chat = self.__BD_Chats.getByID(id)
        if chat != None:
            chat.setIDAccounts(idAcc)

    # Выдача списка ID аккаунтов по ID
    def getChatIDAccounts(self, id):
        chat = self.__BD_Chats.getByID(id)
        if chat != None:
            return chat.getPassword()

    # Добавление ID в список ID аккаунтов
    def addAccountIDtoChat(self, id, idAcc):
        chat = self.__BD_Chats.getByID(id)
        if chat != None:
            myAccount = self.__BD_Accounts.getByID(idAcc)
            if myAccount != None:
                ID_List = chat.getIdAccounts()
                ID_List.addId(myAccount)
                chat.setIdAccounts(ID_List)

    # Удаление ID из списка ID аккаунтов
    def removeAccountByID(self, id, idAcc):
        chat = self.__BD_Chats.getByID(id)
        if chat != None:
            if self.__BD_Accounts.getByID(idAcc) != None:
                chat.removeAccountByID(idAcc)


# Создание класса для работы с файлом, в которым находится база данных с аккаунтами
class DataBase_TXT(DataBase):

    # Добавление аккаунта в файл
    def save(self, path):
        file = open(path, 'w')  # Открытие файла
        for account in self.getAccountList():
            file.write(
                f'{account.getID()}|{account.getLogin()}|{account.getPassword()}|{account.getPincode()}\n')  # То что мы добавляем
        file.close()  # Закрываем файл

    # Просмотр аккаунтов в файле
    def load(self, path):
        file = open(path, 'r')  # Открытие файла
        for line in file:  # Перебираем строчки в файле
            val = line.split('|')
            acc = Account(int(val[0]), val[1], val[2], val[3][:-1])
            self.addAccount(acc)
        file.close()  # Закрытие файла


class DataBase_JSON(DataBase):

    # Добавление данных в файл
    def save(self, path):
        if path.endswith('.json'):  # Проверка на тип данных
            accountss = []  # Создание списка с аккаунтами
            for account in self.getAccountList():
                # Создание словаря с данными определённого акккаунта
                slovarik = {
                    'id': account.getID(),
                    'login': account.getLogin(),
                    'password': account.getPassword(),
                    'pincode': account.getPincode()
                }
                accountss.append(slovarik)  # Добавление в список аккаунтов словарь с данными
            chats = []  # Создание списка с чатами
            for chat in self.getChatList():
                # Создание словаря с данными определённого чата
                slovar = {
                    'id': chat.getID(),
                    'name': chat.getName(),
                    'idAccounts': chat.getIdAccounts()
                }
                chats.append(slovar)  # Добавление словаря с данными в список с чатами
            creatures = {'Accounts': accountss, 'Chats': chats}  # Сущности

            with open(path, 'w') as file:  # Открываем файла
                js.dump(creatures, file)  # Запихываем туда всех сущностей
        else:
            print('Bad')

    # Просмотр файла
    def load(self, path):
        if path.endswith('.json'):  # Проверка на тип данных
            self.clear()  # Очистка (на всякий)
            with open(path, 'r') as file:  # Открытие файла
                creatures = js.load(file)  # Сохраняем в переменную содержание файла (в нашем случае это сущности)
                for acc in creatures['Accounts']:  # Перебираем аккаунты из переменной с сущностями
                    # Создание переменной с аккаунтом
                    account = Account(
                        acc['id'],
                        acc['login'],
                        acc['password'],
                        acc['pincode']
                    )
                    self.addAccount(account)  # Добавление аккаунта
