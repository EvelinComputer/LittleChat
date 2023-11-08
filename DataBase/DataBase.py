import logging as log
import pymysql

class DataBase_MySQL:

    def __init__(self):
        self.__DB = pymysql.connect(user='user', password='1234', host='127.0.0.1', database='LittleChat')
        self.__Cursor = self.__DB.cursor()

    """ 
        Метод проверяет на наличие этого аккаунта 
        Аргумент: login логин
        Аргумент: password пароль
        Возвращает: 
            bool - состояние авторизации
            str - сообщение состояния
    """
    def checkAccount(self, login, password):
        self.__Cursor.execute("""SELECT * FROM `Account` WHERE `Login` LIKE '{0}'""" .format(login))
        l = self.__Cursor.fetchall()
        if len(l) > 0:
            if l[0][2] == password:
                sms = ' Авторизиция прошла успешно!'
                log.info(sms)
                return True, sms
            else:
                sms = ' Неверный пароль'
                log.error(sms)
                return False, sms
        sms = ' Аккаунта с таким логином не существует'
        log.error(sms)
        return False, sms


    def newAccount(self, login, password, last_name, first_name, phone_number, email, pincode):
        #self.__Cursor.execute("""INSERT INTO `Account.txt` (`ID`, `Login`, `Password`, `LastName`, `FirstName`,
        # `PhoneNumber`, `Email`, `PinCode`, `RegData`) VALUES (NULL, '{0}', '{1}', '{2}', '{3}',
        #  '{4}', '{5}', {6}, CURRENT_TIMESTAMP);"""
        #  .format(id, login, password, last_name, first_name, phone_number, email, pincode))

        """ @TODO Добавить проверку заполнения полей!!! """
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