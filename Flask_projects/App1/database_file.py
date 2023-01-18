import mysql.connector

class database():
    def __init__(self):
        self.__connection = mysql.connector.connect(host="localhost",port="3300",user="root",password="root123",database="python_test_flask_db")
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def store_data(self,query):
        self.__cursor.execute(query)
        self.__connection.commit()

    def read_data(self,query):
        self.__cursor.execute(query)
        return self.__cursor.fetchall()
