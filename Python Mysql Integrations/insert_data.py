import mysql.connector

conn = mysql.connector.connect(host="localhost",user="root",password="avi#12345",port=3307,database="python_db")

if conn.is_connected():
    print("Connected to MySQL database")

mycursor = conn.cursor()

sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
val = [("John Doe", "john.doe@example.com"),('Rojarani', 'roja@gmail.com'),('Avi', 'avi@gmail.com')]

mycursor.executemany(sql, val)

conn.commit()

print(mycursor.rowcount, "record inserted.")

