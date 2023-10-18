import logging as log
import json as js
from DataBase.Chat import Chat, ChatList, IdAccounts
from DataBase.Account import Account, AccountList
import sqlite3 as SQL
import pymysql

# Создание полноценной базы данных
class DataBase:
    __BD_Accounts = AccountList()  # Это просто список аккаунтов
    __BD_Chats = ChatList()  # А это список чатов

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
        Acc = self.__BD_Accounts.getByID(id)  # Получаем аккаунт по его ID
        if Acc != None:  # Проверка на существование аккаунта
            return Acc

    # Удаление аккаунта из базы данных по ID
    def removeAccount(self, id):
        self.__BD_Accounts.removeAccountByID(id)

    # Установка логина для аккаунта по ID
    def setAccountLogin(self, id, login):
        Acc = self.__BD_Accounts.getByID(id)  # Получаем аккаунт по его ID
        if Acc != None:  # Проверка на существование аккаунта
            return Acc.setLogin(login)

    # Выдача логина аккаунта по ID
    def getAccountLogin(self, id):
        Acc = self.__BD_Accounts.getByID(id)  # Получаем аккаунт по его ID
        if Acc != None:  # Проверка на существование аккаунта
            return Acc.getLogin()

    # Установка пароля для аккаунта по ID
    def setAccountPassword(self, id, password):
        Acc = self.__BD_Accounts.getByID(id)  # Получаем аккаунт по его ID
        if Acc != None:  # Проверка на существование аккаунта
            return Acc.setPassword(password)

    # Выдача пароля аккаунта по ID
    def getAccountPassword(self, id):
        Acc = self.__BD_Accounts.getByID(id)  # Получаем аккаунт по его ID
        if Acc != None:  # Проверка на существование аккаунта
            return Acc.getPassword()

    # Установка пинкода для аккаунта по ID
    def setAccountPincode(self, id, pincode):
        Acc = self.__BD_Accounts.getByID(id)  # Получаем аккаунт по его ID
        if Acc != None:  # Проверка на существование аккаунта
            return Acc.setPincode(pincode)

    # Выдача пинкода аккаунта по ID
    def getAccountPincode(self, id):
        Acc = self.__BD_Accounts.getByID(id)  # Получаем аккаунт по его ID
        if Acc != None:  # Проверка на существование аккаунта
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
        chat = self.__BD_Chats.getByID(id)  # Получение чата по его ID
        if chat != None:  # Проверка на существование
            return chat

    # Удаление чата из базы данных по ID
    def removeChat(self, id):
        self.__BD_Chats.removeAccountByID(id)

    # Установка наименования чата
    def setChatName(self, id, name):
        chat = self.__BD_Chats.getByID(id)  # Получение чата по его ID
        if chat != None:
            chat.setName(name)

    # Выдача наименования чата по ID
    def getChatName(self, id):
        chat = self.__BD_Chats.getByID(id)  # Получение чата по его ID
        if chat != None:  # Проверка на существование
            return chat.getName()

    # Установка списка ID аккаунтов по ID
    def setChatIDAccounts(self, id, idAcc):
        chat = self.__BD_Chats.getByID(id)  # Получение чата по его ID
        if chat != None:  # Проверка на существование
            chat.setIDAccounts(idAcc)

    # Выдача списка ID аккаунтов по ID
    def getChatIDAccounts(self, id):
        chat = self.__BD_Chats.getByID(id)  # Получение чата по его ID
        if chat != None:  # Проверка на существование
            return chat.getPassword()

    # Добавление ID в список ID аккаунтов
    def addAccountIDtoChat(self, id, idAcc):
        chat = self.__BD_Chats.getByID(id)  # Получение чата по его ID
        if chat != None:  # Проверка на существование чата
            myAccount = self.__BD_Accounts.getByID(idAcc)
            if myAccount != None:  # Проверка на существование аккаунта
                ID_List = chat.getIdAccounts()  # Получение списка ID аккаунтов
                ID_List.addId(myAccount)  # Добавление аккаунта
                chat.setIdAccounts(ID_List)  # Обновление списка ID аккаунта

    # Удаление ID из списка ID аккаунтов
    def removeAccountByID(self, id, idAcc):
        chat = self.__BD_Chats.getByID(id)  # Получение чата по его ID
        if chat != None:  # Проверка на существование чата
            if self.__BD_Accounts.getByID(idAcc) != None:  # Проверка на существование аккаунта
                chat.removeAccountByID(idAcc)  # Удаление аккаунта


# Создание класса для работы с файлом, в которым находится база данных с аккаунтами
class DataBase_TXT(DataBase):

    # Добавление аккаунта в файл
    def save(self, path):
        file = open(path, 'w')  # Открытие файла
        for account in self.getAccountList():  # Перебор аккаунтов из списка аккаунтов
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

                for chat in creatures['Chats']:  # Перебор чатов из переменной с сущностями
                    # Создание переменной с чатом
                    chat = Chat(
                        chat['id'],
                        chat['name'],
                        chat['idAccounts'],
                    )
                    self.addChat(chat)  # Добавление чата


class DataBase_SQL(DataBase):

    def save(self, path):
        DB = SQL.connect(path)  # "заходим" в файл с помощью пути
        Cursor = DB.cursor()  # Создание курсора

        # Создаём таблицу (ы)
        Cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts (id INT, login TEXT, password TEXT, pincode TEXT)""")
        Cursor.execute("""CREATE TABLE IF NOT EXISTS Chats (id INT, name TEXT)""")
        Cursor.execute("""CREATE TABLE IF NOT EXISTS Permissions (id INT, idChat INT, idAccount INT)""")
        DB.commit()  # Подтверждение изменений

        # Удаление
        Cursor.execute("""DELETE FROM Accounts""")
        Cursor.execute("""DELETE FROM Chats""")
        Cursor.execute("""DELETE FROM Permissions""")
        DB.commit()

        # Cохранение базы данных аккаунтов
        for acc in self.getAccountList():
            # Добавление
            Cursor.execute("""INSERT INTO Accounts ("id", "login", "password", "pincode") VALUES ({0}, '{1}', '{2}', '{3}')"""
                           .format(acc.getID(), acc.getLogin(), acc.getPassword(), acc.getPincode()))
            DB.commit()

        ID_Permission = 0
        # Сохранение базы данных чатов
        for chat in self.getChatList():
            # Добавление
            Cursor.execute("""INSERT INTO Chats ("id", "name") VALUES ({0}, '{1}')"""
                           .format(chat.getID(), chat.getName()))
            for id_acc in chat.getIdAccounts():
                Cursor.execute("""INSERT INTO Permissions ("id", "idChat", "idAccount") VALUES ({0}, {1}, {2})"""
                               .format(ID_Permission, chat.getID(), id_acc))
                ID_Permission += 1
            DB.commit()


        #Cursor.execute("""INSERT INTO Accounts ("id", "login", "password", "pincode") VALUES (12, 'fdsf', '12123', '2312')""")
        #DB.commit()


    def load(self, path):
        DB = SQL.connect(path)  # "заходим" в файл с помощью пути
        Cursor = DB.cursor()  # Создание курсора

        # Ну и дальше находим элемент и добавляем его в соответствующую часть базы данных
        for account in Cursor.execute("""SELECT * FROM Accounts"""):
            self.addAccount(Account(account[0], account[1], account[2], account[3]))

        for chat in Cursor.execute("""SELECT * FROM Chats"""):
            self.addChat(Chat(chat[0], chat[1]))

        for permission in Cursor.execute("""SELECT * FROM Permissions"""):
            self.addAccountIDtoChat(permission[1], permission[2])


class DataBase_MySQL:
    def __init__(self):
        self.__DB = pymysql.connect(user='user', password='1234', host='127.0.0.1', database='LittleChat')
        self.__Cursor = self.__DB.cursor()

    #def ()
    def checkAccount(self, login, password):
        self.__Cursor.execute("""SELECT * FROM `Account` WHERE `Login` LIKE '{0}'"""
                              .format(login))
        l = self.__Cursor.fetchall()
        if len(l) > 0:
            if l[0][2] == password:
                print('Авторизировалось')
            else:
                print('Пароль не совпал')
        else:
            print('Аккаунта не существует')


    def newAccount(self, login, password, last_name, first_name, phone_number, email, pincode):
        #self.__Cursor.execute("""INSERT INTO `Account` (`ID`, `Login`, `Password`, `LastName`, `FirstName`,
        # `PhoneNumber`, `Email`, `PinCode`, `RegData`) VALUES (NULL, '{0}', '{1}', '{2}', '{3}',
        #  '{4}', '{5}', {6}, CURRENT_TIMESTAMP);"""
        #  .format(id, login, password, last_name, first_name, phone_number, email, pincode))

        self.__Cursor.execute("""INSERT INTO `Account` (`ID`, `Login`, `Password`, `LastName`, `FirstName`,
                 `PhoneNumber`, `Email`, `PinCode`, `RegData`) VALUES (NULL, '{0}', '{1}', '{2}', '{3}',
                  '{4}', '{5}', {6}, CURRENT_TIMESTAMP);"""
                  .format(login, password, last_name, first_name, phone_number, email, pincode))

        l = self.__Cursor.fetchall()
        self.__DB.commit()
        print('Работает')