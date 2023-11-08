from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, QTimer

import datetime as dt

class MyLittleButton(QMainWindow):

    __counter = 0
    __vector = True

    def __setColorButton(self, colorG):

        MyStyle_1 =  'QPushButton{\n'\
                       'background:  rgb(170, ';
        MyStyle_2 =     ', 255);\n'\
                       'border-radius: 25px;\n'\
                       'color: rgb(100, 49, 171);\n' \
                       '}\n'\
                       'QPushButton:hover{\n'\
                       'background: rgb(141, 88, 221);\n'\
                       'border-radius: 25px;\n'\
                       'color:rgb(68, 34, 116);\n'\
                       '}\n'\
                       'QPushButton:pressed{\n'\
                       'background: rgb(37, 18, 75);\n'\
                       'border-radius: 25px;\n'\
                       'color:rgb(141, 88, 221);\n'\
                       '}'

        return MyStyle_1 + str(colorG) + MyStyle_2

    def __init__(self):
        super(MyLittleButton, self).__init__()  # Наследуем конструктор QMainWindow
        uic.loadUi("./MyButton.ui", self)  # Загружаем UI форму (Qt Designer)

        self.__timer = QTimer()

        self.__timer.timeout.connect(self.tick)
        self.B_Click.clicked.connect(self.funcClick)

        self.__timer.start(5)

    def tick(self):
        #print(dt.datetime.now(), self.__counter)
        if self.__counter <= 0:
            self.__vector = True
        if self.__counter >= 200:
            self.__vector = False
        if self.__vector:
            self.__counter += 1
        else:
            self.__counter -= 1
        self.B_Click.setStyleSheet(self.__setColorButton(self.__counter))
        #print(self.B_Click.styleSheet())

    def funcClick(self):
        if self.__timer.isActive():
            self.__timer.stop()
        else:
            self.__timer.start()