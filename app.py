from flask import Flask, render_template, redirect, request, session, url_for
from cart import Cart
from billing import calculate_bill
from db import get_connection

app = Flask(__name__)
app.secret_key = 'mysecretkey'
cart = Cart()

@app.route("/", methods=["GET"])
def root():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                if user and user['password'] == password:
                    session['user'] = user['username']
                    return redirect("/home")
                else:
                    return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
        return redirect("/login")

    return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if 'user' not in session:
        return redirect("/login")

    search_query = request.form.get("search") if request.method == "POST" else ""
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            if search_query:
                cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{search_query}%",))
            else:
                cursor.execute("SELECT * FROM products")
            all_products = cursor.fetchall()

    groceries = [p for p in all_products if p['category'] == 'groceries']
    electronics = [p for p in all_products if p['category'] == 'electronics']

    return render_template("index.html",
                           groceries=groceries,
                           electronics=electronics,
                           username=session['user'],
                           search=search_query)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    if 'user' not in session:
        return redirect("/login")
    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                cart.add_item(product, quantity)
    return redirect("/home")

@app.route("/cart")
def view_cart():
    if 'user' not in session:
        return redirect("/login")
    return render_template("cart.html", cart=cart.get_items(), username=session['user'])

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    if 'user' not in session:
        return redirect("/login")
    cart.remove_item(product_id)
    return redirect("/cart")

@app.route("/clear-cart")
def clear_cart():
    if 'user' not in session:
        return redirect("/login")
    cart.clear_cart()
    return redirect("/cart")

@app.route("/bill")
def show_bill():
    if 'user' not in session:
        return redirect("/login")

    cart_items = cart.get_items()
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            for item in cart_items:
                product_id = item['product']['id']
                quantity = item['quantity']

                cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
                stock = cursor.fetchone()['stock']

                if stock >= quantity:
                    cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (quantity, product_id))
                else:
                    item['quantity'] = 0
            connection.commit()

    cart.items = [item for item in cart_items if item['quantity'] > 0]
    bill = calculate_bill(cart.get_items())
    cart.clear_cart()
    return render_template("bill.html", bill=bill, username=session['user'])

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)



#this project is done by Muthuharish Sreenithi Nisha and Pathumaaaa 