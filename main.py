from PyQt6.QtWidgets import QApplication
from LittleChat import LittleChat

def Main():

    # Запуск QT ядра
    App = QApplication([])

    # Создание окна
    Soft = LittleChat()

    # Показ окна
    Soft.start()

    # Запуск
    App.exec()



if __name__ == "__main__": Main()