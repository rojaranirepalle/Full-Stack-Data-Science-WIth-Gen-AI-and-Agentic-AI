import mysql.connector

conn = mysql.connector.connect(host="localhost",user="root",password="avi#12345",port=3307,database="python_db")

if conn.is_connected():
    print("Connected to MySQL database")

mycursor = conn.cursor()

mycursor.execute("CREATE table IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)
