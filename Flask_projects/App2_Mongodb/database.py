from pymongo import MongoClient
import pandas as pd

class database():

    def __init__(self):
        self.__connection = MongoClient("localhost",27017)

        self.__cursor = self.__connection.get_database("mongotest")
    def __del__(self):
        del self.__cursor
        self.__connection.close()
    # {"coll": "user",{"_id": 1,"Name":"dhawal","LastName":"Patel","addr":"pune"}}
    # {"coll": "product",{"_id": 1,"ProductName":"dhawal","ProductCategory":"Patel","description":"pune"}}
    def insert_data(self,data):
        # selecting collections first
        if data.get("coll") == "user":
            coll = self.__cursor.get_collection("user")
            coll.insert_one({
                "_id": data[1].get("_d"),
                "Name": data[1].get("Name"),
                "LastName": data[1].get("LastName"),
                "addr": data[1].get("addr")
            })
        if data.get("coll") == "product":
            coll = self.__cursor.get_collection("product")
            coll.insert_one({
                "_id": data[1].get("_d"),
                "ProductName": data[1].get("ProductName"),
                "ProductCategory": data[1].get("ProductCategory"),
                "description": data[1].get("description")
            })
    # {"coll": "user","find":{"lastName": "patel"}}
    def read_data(self,query):
        # selecting collection from which data to want to fetch
        if(query.get("coll")=="user"):
            coll = self.__cursor.get_collection("user")
            list00 = coll.find(query.get("find"))
            return list00
        elif(query.get("coll")=="product"):
            coll = self.__cursor.get_collection("product")
            list00 = coll.find(query.get("find"))
            return list(list00)