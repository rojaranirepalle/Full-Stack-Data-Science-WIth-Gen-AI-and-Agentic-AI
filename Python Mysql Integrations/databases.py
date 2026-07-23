import mysql.connector

conn = mysql.connector.connect(host="localhost",user="root",password="avi#12345",port=3307)

mycursor = conn.cursor()

mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)