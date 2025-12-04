import mysql.connector
from mysql.connector import Error

def create_connection():
    
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='cinema_db',  
            user='root',           
            password=''            
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    return connection