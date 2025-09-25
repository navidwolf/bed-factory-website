from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # برای مدیریت session

# داده‌های نمونه محصولات
products = [
    {"id": 1, "name": "تخت خواب 1", "price": 1200000, "image": "product1.webp", "rating": 4.5, "tag": "جدید"},
    {"id": 2, "name": "تخت خواب 2", "price": 1500000, "image": "product2.webp", "rating": 4.0, "tag": ""},
    {"id": 3, "name": "تخت خواب 3", "price": 900000, "image": "product3.webp", "rating": 3.5, "tag": "پرفروش"},
    {"id": 4, "name": "تخت خواب 4", "price": 1100000, "image": "product4.webp", "rating": 4.2, "tag": ""},
    {"id": 5, "name": "تخت خواب 5", "price": 1300000, "image": "product5.webp", "rating": 4.7, "tag": "جدید"},
    {"id": 6, "name": "تخت خواب 6", "price": 1250000, "image": "product6.webp", "rating": 4.1, "tag": ""},
    {"id": 7, "name": "تخت خواب 7", "price": 1400000, "image": "product7.webp", "rating": 3.9, "tag": "پرفروش"},
    {"id": 8, "name": "تخت خواب 8", "price": 1000000, "image": "product8.webp", "rating": 4.3, "tag": ""}
]


def get_cart():
    return session.get("cart", [])


def save_cart(cart):
    session["cart"] = cart


@app.route("/")
def index():
    return render_template("index.html", products=products)


@app.route("/products")
def products_page():
    return render_template("products.html", products=products)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    return render_template("product_detail.html", product=product)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    cart_items = get_cart()
    if request.method == "POST":
        # بروزرسانی تعداد محصولات
        updated_cart = []
        for item in cart_items:
            qty_str = request.form.get(f"quantity_{item['id']}")
            if qty_str and qty_str.isdigit():
                qty = int(qty_str)
                if qty > 0:
                    item["quantity"] = qty
                    updated_cart.append(item)
        save_cart(updated_cart)
        return redirect(url_for("cart"))
    return render_template("cart.html", cart_items=cart_items)


@app.route("/checkout")
def checkout():
    cart_items = get_cart()
    return render_template("checkout.html", cart_items=cart_items)


@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart_items = get_cart()
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        existing = next((item for item in cart_items if item["id"] == product_id), None)
        if existing:
            existing["quantity"] += 1
        else:
            cart_items.append({**product, "quantity": 1})
    save_cart(cart_items)
    return redirect(url_for("cart"))


@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart_items = [item for item in get_cart() if item["id"] != product_id]
    save_cart(cart_items)
    return redirect(url_for("cart"))


@app.route("/contact")
def contact():
    return "صفحه تماس با ما"


# ---- Admin routes ----
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "1234":
            return redirect(url_for("admin_dashboard"))
    return render_template("admin/login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html", products=products, cart_items=get_cart())


if __name__ == "__main__":
    app.run(debug=True)
