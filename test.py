import pymysql

db = pymysql.connect(user='user', password='1234', host='127.0.0.1', database='Test')
cursor = db.cursor()

info = cursor.execute('SELECT * FROM example')
rows = cursor.fetchall()

#for item in rows:
#    print(item)

#cursor.execute("""INSERT INTO `example` (`ID`, `Text`, `Secret`, `Data`) VALUES (NULL, '{0}', '{1}', CURRENT_TIMESTAMP);"""
               #.format("User", "1254"))
#db.commit()

cursor.execute("""""")
l = cursor.fetchall()

for item in l:
    cursor.execute("""UPDATE `example` SET `Text` = 'Privet' WHERE `example`.`ID` = {0};"""
                   .format(item[0]))
    db.commit()

cursor.execute("""SELECT * FROM example""")
l2 = cursor.fetchall()

listik = []
for item in l2:
    if listik.count(item[1]) == 0:
        listik.append(item[1])
    else:
        cursor.execute("""DELETE FROM example WHERE `example`.`ID` = {0}"""
                       .format(item[0]))
        db.commit()
    #print(item)

for item in listik:
    print(item, listik.count(item))