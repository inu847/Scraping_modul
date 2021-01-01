import mysql.connector

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="",
                               database="test")

if mydb.is_connected:
  print('Koneksi berhasil')

  sql = "insert into message(comment) values (%s)"

  mycursor = mydb.cursor()
  data = ('John', 'hallo')
  mycursor.execute(sql, data)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")