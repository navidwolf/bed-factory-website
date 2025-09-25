from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # ضروری برای session

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

# افزودن به سبد خرید
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        if "cart_items" not in session:
            session["cart_items"] = []
        cart_items = session["cart_items"]
        existing = next((item for item in cart_items if item["id"] == product_id), None)
        if existing:
            existing["quantity"] += 1
        else:
            cart_items.append({**product, "quantity": 1})
        session["cart_items"] = cart_items
    return redirect(url_for("cart"))

# نمایش سبد خرید و بروزرسانی تعداد
@app.route("/cart", methods=["GET", "POST"])
def cart():
    cart_items = session.get("cart_items", [])
    if request.method == "POST":
        for item in cart_items[:]:
            qty_str = request.form.get(f"quantity_{item['id']}")
            if qty_str and qty_str.isdigit():
                qty = int(qty_str)
                if qty > 0:
                    item["quantity"] = qty
                else:
                    cart_items.remove(item)
        session["cart_items"] = cart_items
        return redirect(url_for("cart"))
    return render_template("cart.html", cart_items=cart_items)

# حذف محصول از سبد
@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart_items = session.get("cart_items", [])
    cart_items = [item for item in cart_items if item["id"] != product_id]
    session["cart_items"] = cart_items
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_items = session.get("cart_items", [])
    if request.method == "POST":
        # اینجا می‌توانید عملیات پرداخت و ذخیره سفارش را انجام دهید
        session["cart_items"] = []  # پاک کردن سبد پس از خرید
        return redirect(url_for("index"))
    return render_template("checkout.html", cart_items=cart_items)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        print(f"New message from {name} ({email}): {message}")
        return redirect(url_for("contact"))
    return render_template("contact.html")

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
    cart_items = session.get("cart_items", [])
    return render_template("admin/dashboard.html", products=products, cart_items=cart_items)

if __name__ == "__main__":
    app.run(debug=True)
