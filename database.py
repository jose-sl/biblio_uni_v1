import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        # connection = mysql.connector.connect(
        #     host="localhost",
        #     port=1106,
        #     user="seminario",
        #     password="seminario123",
        #     database="biblio_uni"
        # )

        connection = mysql.connector.connect(
            host="sql5.freesqldatabase.com",
            port=3306,
            user="sql5837287",
            password="Ffx6BuTmCE",
            database="sql5837287"
        )

        return connection

    except Error as e:
        print(f"Error de conexión: {e}")
        return None