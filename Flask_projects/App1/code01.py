from flask import Flask,render_template,redirect,request
import database_file as database
def function01():

    app = Flask(__name__)
    @app.route("/",methods=["GET"])
    def root():
        return "<h1 style=\" color:red; font-size:50px\">Welcome to this page</h1>"

    app.run(host="localhost",port="4000",debug=True)

# function01()

def function02():
    app = Flask(__name__)
    @app.route("/",methods=["GET"])
    def root():
        return render_template("login.html")

    @app.route("/register",methods=["GET"])
    def register_user():
        return render_template("register.html")

    @app.route("/register-user-data",methods=["POST"])
    def register_user_data():
        db = database.database()

        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        query =  f"insert into user (firstName,lastName,email,password) value('{first_name}','{last_name}','{email}','{password}');"
        print(query)

        db.store_data(query)
        del db

        return redirect("/")

    @app.route("/home",methods=["GET"])
    def home():
        db = database.database()

        query = f"select id,title,description,price from product;"

        products = db.read_data(query)
        print(products)

        del db

        # return redirect("index.html",products=products)
        return render_template("index.html",products=products)

    @app.route("/add-product",methods=["GET"])
    def add_product():
        print("inside app-product page function")
        return render_template("add_product.html")

    @app.route("/add-product-data",methods=["POST"])
    def add_product_data():
        db = database.database()
        product_title = request.form.get("title")
        product_price = request.form.get("price")
        product_des = request.form.get("description")

        query = f"insert into product (title,price,description) values('{product_title}','{product_price}','{product_des}');"
        db.store_data(query)
        del db
        return redirect("/home")

    @app.route("/login",methods=["GET"])
    def login_page():
        return render_template("login.html")

    @app.route("/login-data",methods=["POST"])
    def login_data():
        db = database.database()
        email = request.form.get('email')
        print(email)
        query = f"select * from user where email='{email}';"
        print(query)
        user_valid = db.read_data(query)
        print(user_valid)
        del db
        if(len(user_valid)>0):
            return ("<h1>yes! your are Here</h1>")
        else:
            return "<h1>you are not register, go to register page</h1>"

    app.run(host="localhost",port="4000",debug=True)


function02()