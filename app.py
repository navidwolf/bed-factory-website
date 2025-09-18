from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # حتماً توی حالت واقعی تغییرش بده

# دیتای محصولات
products = [
    {"id": 1, "name": "تشک طبی مدل A", "price": 2500000, "old_price": 2800000, "image": "product1.webp"},
    {"id": 2, "name": "تخت خواب دو نفره مدل B", "price": 4800000, "old_price": 5200000, "image": "product2.webp"},
    {"id": 3, "name": "کالای خواب لوکس مدل C", "price": 3500000, "old_price": 3900000, "image": "product3.webp"},
    {"id": 4, "name": "تشک فنری مدل D", "price": 1800000, "old_price": 2000000, "image": "product4.webp"},
    {"id": 5, "name": "تخت یک نفره مدل E", "price": 2200000, "old_price": 2500000, "image": "product5.webp"},
    {"id": 6, "name": "سرویس خواب مدل F", "price": 5600000, "old_price": 6000000, "image": "product6.webp"},
    {"id": 7, "name": "تشک طبی فنری مدل G", "price": 2700000, "old_price": 3000000, "image": "product7.webp"},
    {"id": 8, "name": "کالای خواب ارگونومیک مدل H", "price": 3900000, "old_price": 4200000, "image": "product8.webp"},
]

@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/products")
def product_list():
    return render_template("products.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    return render_template("product_detail.html", product=product, products=products)

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items, total = [], 0
    for pid, qty in cart.items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            cart_items.append({"product": product, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", cart_items=cart_items, total=total)

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})
    cart_items, total = [], 0
    for pid, qty in cart.items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            cart_items.append({"product": product, "qty": qty, "subtotal": subtotal})

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        session.pop("cart", None)
        return render_template("checkout.html", success=True, name=name)

    return render_template("checkout.html", cart_items=cart_items, total=total, success=False)

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
