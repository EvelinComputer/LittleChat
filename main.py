from PyQt6.QtWidgets import QApplication
from DataBase.DataBase import DataBase_JSON, DataBase_SQL, DataBase_MySQL
from DataBase.Account import AccountList, Account
from DataBase.Chat import ChatList, Chat, IdAccounts

from AutorisWindow.AutorisWindow import AutorisWindow

def Main():
    #App = QApplication([])

    MyDB = DataBase_MySQL()

    Login = "Pancake"
    Passwd = "1234567"

    # MyDB.checkAccount(Login, Passwd)
    #MyDB.newAccount('qew', '12345', 'Polwle', 'Koewkq', '+8786566',
    #                'feqeq@mail.ru', 7469)


    #DB = DataBase_SQL()  # Создание базы данных
    #DB.load('DataBase.db')
    # Добавление аккаунтов
    # DB.addAccount(Account(0, 'wqe', '1256', '1234'))
    # print(DB.lenAccounts())
    #DB.addAccount(Account(2, 'fgsdf', '128879', '2567'))
    ## Добавление чатов
    #DB.addChat(Chat(0, 'Chat'))
    #DB.addChat(Chat(1, 'Ne chat'))
    ## Добавление ID аккаунтов
    #DB.addAccountIDtoChat(0, 1)
    #DB.addAccountIDtoChat(0, 2)
    #DB.addAccountIDtoChat(1, 2)
    #DB.save("DataBase.db")  # Сохранение
    #DB.clear()  # Очищение
    #DB.load("DataBase.db")  # Восстановление (или как это назвать?)

    # Выведение данных в консоль
    #for acc in DB.getAccountList():
    #    print(acc)
    #for chat in DB.getChatList():
    #    print(chat)

    DB = DataBase_JSON()        # Создали объект базы данных

    # Будет загрузка БД !!!

    Win = AutorisWindow(DB)  # Создание окна
    #Win.setWindowTitle("Авторизация")  # Меняем название окна
    print('dada')
    Win.show()  # Показ окна

    #App.exec()



if __name__ == "__main__": Main()