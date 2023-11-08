from PyQt6.QtWidgets import QApplication
from DataBase.DataBase import DataBase_MySQL
from AutorisWindow.AutorisWindow import AutorisWindow
from Server.Server import LittleChatServer

def Main():

    # Запуск QT ядра
    App = QApplication([])

    # Подключение к серверу
    Server = LittleChatServer()

    # Создание окна
    Win = AutorisWindow(Server)

    # Показ окна
    Win.showFullScreen()

    # Запуск
    App.exec()



if __name__ == "__main__": Main()