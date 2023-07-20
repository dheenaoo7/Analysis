import mysql.connector
import time
mydb = mysql.connector.connect(
    host="analysis.cyufabl1vpsa.ap-northeast-1.rds.amazonaws.com",
    user="admin",
    password="admin123",
    database="analysis"
)
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE IF NOT EXISTS analysis")

def create_table(table_name, data):
    mycursor = mydb.cursor()
    keys = data
    columns = ', '.join([f"`{key}` VARCHAR(30)" for key in keys])
    query = f"CREATE TABLE {table_name} ({columns})"
    mycursor.execute(query)
    mycursor.close()


t=str(time.localtime().tm_yday)
print(time.localtime().tm_yday)
