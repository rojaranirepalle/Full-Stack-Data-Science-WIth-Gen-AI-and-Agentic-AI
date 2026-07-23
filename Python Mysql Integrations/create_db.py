import mysql.connector

conn = mysql.connector.connect(host="localhost",user="root",password="avi#12345",port=3307)

if conn.is_connected():
    print("Connected to MySQL database")

mycursor = conn.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS python_db")
print(mycursor)
print("Database created successfully")
