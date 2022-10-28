from datetime import datetime

from flask import Flask,render_template, request,redirect

import psycopg2

# create an object
app = Flask(__name__)

#Connect to an existing database
conn = psycopg2.connect(user="postgres", password="12345", host="localhost", port="5432", database="postgres")

# a connection creates a session.
#a session is the period in which you’re  connected or logged in into your db. 
#Open a cursor to perform database operations
cur = conn.cursor()

# home route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#admin dashboard
@app.route("/admin/dashboard", methods=["GET"])
def dashboard():
    return render_template("admin/dashboard.html")

#admin inventories
@app.route("/admin/inventories", methods=["GET","POST"])
def inventories():
    if request.method == "POST":
        #To capture data from the form
        name = request.form["name"]
        quantity = request.form["quantity"]
        bp = request.form["bp"]
        sp = request.form["sp"]
        # Inserting data to database
        cur = conn.cursor()
        cur.execute("INSERT INTO inventories (name,quantity, bp, sp) VALUES (%s, %s, %s, %s)",(name,quantity,bp,sp))
        conn.commit()
        # redirecting is a get request
        return redirect("/admin/inventories") 
    else:
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventories")
        data = cur.fetchall()
        print(data)
        return render_template("admin/inventories.html",data = data)

#Sales route
@app.route("/admin/sales", methods=["GET","POST"])
def sales():  
    
    cur.execute("SELECT * FROM sales")
    saledata = cur.fetchall()
    print(saledata)  
    return render_template("admin/sales.html",saledata=saledata)

#Make a Sale
@app.route("/make_sales", methods=["GET","POST"])
def make_sales():
    if request.method == "POST":
        #To capture data from the form
        pid = request.form["pid"]
        quantity = request.form["quantity"]
        created_at = datetime.now()
        
        # Inserting data to database
        cur = conn.cursor()
        cur.execute("INSERT INTO sales (pid,quantity, created_at) VALUES (%s, %s, %s)",(pid,quantity,created_at))
        conn.commit()
        # redirecting is a get request
        return redirect("admin/sales") 
    else:

        cur = conn.cursor()
        cur.execute("SELECT * FROM sales")
        saledata = cur.fetchall()
        print(saledata)
        return render_template("admin/sales.html", saledata=saledata)

    #1. Made a template for inventories/sales
    #2. Make a route, then render the template.
    #3. connect to the db and fetch data. print(data)
    #4. using the jinja template you display your data


#View sales
@app.route("/sales/<int:pid>")
def view_sales(pid):
     # query the sales for that product_id
    cur.execute("SELECT * FROM sales WHERE pid=%s;",[pid])
    rows = cur.fetchall()
    return render_template("admin/sales.html", rows = rows) 

