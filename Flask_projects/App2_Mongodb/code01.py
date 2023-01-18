from flask import Flask, render_template,redirect,request
from pymongo import MongoClient
import json
import database as Database

def function01():
    app = Flask(__name__)
    connection = MongoClient("localhost",27017)
    # for coll in connection:
    #     print(coll.)
    # getting list of databases in Mongo server
    for i in connection.list_databases():
        print(i)
    # get database by name:
    db = connection.get_database("mongotest")

    #get collections in Database:
    for coll in db.list_collection_names():
        print(coll)

    #get documents of collection:
    user_coll = db.get_collection("user")

    #get all collection in database:
    for find_11 in user_coll.find():
        print(find_11)

    # get one document by name in collection:
    # doc_1 = list(map(list,user_coll.find({'_id':1})))
    print("finding custom query")
    doc_1 = user_coll.find({"Name":"Dhawal"})

    # for one output use doc_1[0]
    print(doc_1[0])

    #for multiple output it will give list
    #print(doc_1)

# function01()

def function02():
    connection = MongoClient("localhost",27017)
    db = connection.get_database("mongotest")
    collection = db.get_collection("user")
    # for doc in collection.find():
    #     print(doc)
    import pandas as pd
    data = pd.DataFrame(collection.find())
    print(data)

# function02()

def function03():
    app = Flask(__name__)

    @app.route("/",methods=["GET"])
    def home():
        db = Database.database()
        # query = {"coll":"user","find":{"Name":"Dhawal"}}
        query = {"coll":"user","find":""}

        list00 = list(db.read_data(query))
        print(list00)
        value = list00[0].get("addr")
        # print()
        # for i in list00:
        #     print(i)
        del db
        return render_template("home.html",users = list00)

    @app.route("/products",methods=["GET"])
    def products():
        db = Database.database()
        query = {"coll":"product","find":""}
        list00 = list(db.read_data(query))
        print(list00)
        del db

    @app.route("/products/mobiles", methods=["GET"])
    def products():
        db = Database.database()
        # find all products
        # find all
        query = {"coll": "product", "find": ""}
        list00 = list(db.read_data(query))
        print(list00)
        del db
        return render_template("home.html",products = list00)
    app.run(host="localhost",port="4000",debug=True)

function03()

def function04():
    import pandas as pd
    data00 = pd.DataFrame(columns=["id","Name","Addr"])
    data_awsome = {"id":12,"Name":"ritik","Addr":"Mumbai"}
    data02 = pd.DataFrame(data_awsome,columns=["id","Name","Addr"],index=[0])
    print(data02)
    data01 = pd.concat([data00,data02],ignore_index=True,axis=0)
    data01 = pd.concat([data01,data02],ignore_index=True,axis=0)

    # data00.append()

    print(data01)
    # data01 = data00.append({"Name": list00.get("Name"))
    # print(data01)