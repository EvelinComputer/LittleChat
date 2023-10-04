from PyQt6.QtWidgets import QApplication
from DataBase.DataBase import DataBase_JSON
from DataBase.Account import AccountList, Account
from DataBase.Chat import ChatList, Chat, IdAccounts

from AutorisWindow.AutorisWindow import AutorisWindow

def Main():
    App = QApplication([])

    DB = DataBase_JSON()        # Создали объект базы данных

    # Будет загрузка БД !!!

    Win = AutorisWindow(DB)
    Win.setWindowTitle("Авторизация")
    Win.show()

    App.exec()



if __name__ == "__main__": Main()