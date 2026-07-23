import mysql.connector

conn = mysql.connector.connect(host="localhost",user="root",password="avi#12345",port=3307)

if conn.is_connected():
    print("Connected to MySQL database")
print("Connection:", conn)
print(conn.is_connected())