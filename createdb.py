import mysql.connector as mysql

mydb = mysql.connect(
    user='root',
    password='jMwrF!2o7',
    host='localhost',
    port=5000,
    database='users',
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)

mydb.close()