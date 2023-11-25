import logging as log
import pymysql

class DataBase_MySQL:

    def __init__(self, user='user', password='1234', host='127.0.0.1', database='LittleChat'):
        self.reconnect()

    def isConnected(self):
        return self.__ConnectDB

    def reconnect(self, user='user', password='1234', host='127.0.0.1', database='LittleChat'):
        try:
            self.__DB = pymysql.connect(user=user, password=password, host=host, database=database)
            self.__Cursor = self.__DB.cursor()
            self.__ConnectDB = True
        except:
            self.__ConnectDB = False

        return self.__ConnectDB


    """ 
        Метод проверяет на наличие этого аккаунта 
        Аргумент: login логин
        Аргумент: password пароль
        Возвращает: 
            bool - состояние авторизации
            str - сообщение состояния
    """
    def checkAccount(self, login, password):
        try:
            self.__Cursor.execute("""SELECT * FROM `Account` WHERE `Login` LIKE '{0}'""" .format(login))
            l = self.__Cursor.fetchall()
            if len(l) > 0:
                if l[0][2] == password:
                    #sms = f'INFO: {l[0][0]}--{l[0][1]}--{l[0][2]}--{l[0][3]}--{l[0][4]}--{str(l[0][5])}--{l[0][6]}--{l[0][7]}'
                    sms = " Авторизация прошла успешно!"
                    log.info(sms)
                    return True, sms
                else:
                    sms = ' Неверный пароль'
                    log.error(sms)
                    return False, sms
            sms = ' Аккаунта с таким логином не существует'
            log.error(sms)
            return False, sms
        except:
            raise


    def newAccount(self, login, password, last_name, first_name, phone_number, email, pincode):
        #self.__Cursor.execute("""INSERT INTO `Account.txt` (`ID`, `Login`, `Password`, `LastName`, `FirstName`,
        # `PhoneNumber`, `Email`, `PinCode`, `RegData`) VALUES (NULL, '{0}', '{1}', '{2}', '{3}',
        #  '{4}', '{5}', {6}, CURRENT_TIMESTAMP);"""
        #  .format(id, login, password, last_name, first_name, phone_number, email, pincode))

        if '' in [login, password, last_name, first_name, phone_number, email, pincode]:
            sms = 'Заполните ВСЕ поля'
            log.error(sms)
            return False, sms

        self.__Cursor.execute("""INSERT INTO `Account` (`ID`, `Login`, `Password`, `LastName`, `FirstName`,
                 `PhoneNumber`, `Email`, `PinCode`, `RegData`) VALUES (NULL, '{0}', '{1}', '{2}', '{3}',
                  '{4}', '{5}', {6}, CURRENT_TIMESTAMP);"""
                  .format(login, password, last_name, first_name, phone_number, email, pincode))

        l = self.__Cursor.fetchall()
        self.__DB.commit()

        sms = 'Аккаунт успешно создан!'
        log.info(sms)
        return True, sms

    def getNameAccount(self, login):
        try:
            self.__Cursor.execute("""SELECT * FROM `Account` WHERE `Login` LIKE '{0}'""".format(login))
            l = self.__Cursor.fetchall()
            if len(l) > 0:
                # sms = f'INFO: {l[0][0]}--{l[0][1]}--{l[0][2]}--{l[0][3]}--{l[0][4]}--{str(l[0][5])}--{l[0][6]}--{l[0][7]}'
                log.info("Данные об '{0}' переданы!".format(login))
                return [l[0][3], l[0][4]]
            log.error("Логин не найден!")
            return []
        except:
            raise

