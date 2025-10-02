from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

# داده‌های نمونه محصولات
products = [
    {"id": 1, "name": "تخت خواب 1", "price": 1200000, "image": "product1.webp", "rating": 4.5, "tag": "جدید", "short_description": "تختی راحت و با کیفیت عالی."},
    {"id": 2, "name": "تخت خواب 2", "price": 1500000, "image": "product2.webp", "rating": 4.0, "tag": "", "short_description": "خواب راحت با طراحی مدرن."},
    {"id": 3, "name": "تخت خواب 3", "price": 900000, "image": "product3.webp", "rating": 3.5, "tag": "پرفروش", "short_description": "تخت مناسب برای اتاق کوچک."},
    {"id": 4, "name": "تخت خواب 4", "price": 1100000, "image": "product4.webp", "rating": 4.2, "tag": "", "short_description": "کیفیت و راحتی همزمان."},
    {"id": 5, "name": "تخت خواب 5", "price": 1300000, "image": "product5.webp", "rating": 4.7, "tag": "جدید", "short_description": "تخت لوکس و مقاوم."},
    {"id": 6, "name": "تخت خواب 6", "price": 1250000, "image": "product6.webp", "rating": 4.1, "tag": "", "short_description": "راحت و با طراحی کلاسیک."},
    {"id": 7, "name": "تخت خواب 7", "price": 1400000, "image": "product7.webp", "rating": 3.9, "tag": "پرفروش", "short_description": "تخت با کیفیت بالا و قیمت مناسب."},
    {"id": 8, "name": "تخت خواب 8", "price": 1000000, "image": "product8.webp", "rating": 4.3, "tag": "", "short_description": "تخت سبک و جمع و جور."}
]

# هر آیتم سبد، شامل محصول و تعداد آن
cart_items = []

# ---------- صفحات عمومی ----------
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
    if request.method == "POST":
        # بروزرسانی تعداد محصولات
        for item in cart_items[:]:
            qty_str = request.form.get(f"quantity_{item['id']}")
            if qty_str and qty_str.isdigit():
                qty = int(qty_str)
                if qty > 0:
                    item["quantity"] = qty
                else:
                    cart_items.remove(item)
        return redirect(url_for("cart"))
    return render_template("cart.html", cart_items=cart_items)

@app.route("/checkout")
def checkout():
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

# ---------- مدیریت سبد خرید ----------
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        existing = next((item for item in cart_items if item["id"] == product_id), None)
        if existing:
            existing["quantity"] += 1
        else:
            cart_items.append({**product, "quantity": 1})
    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    global cart_items
    cart_items = [item for item in cart_items if item["id"] != product_id]
    return redirect(url_for("cart"))

# ---------- مسیرهای مدیریت ----------
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
    return render_template("admin/dashboard.html", products=products, cart_items=cart_items)

# ---------- Sitemap داینامیک ----------
@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = [
        {"loc": url_for("index", _external=True)},
        {"loc": url_for("products_page", _external=True)},
        {"loc": url_for("cart", _external=True)},
        {"loc": url_for("checkout", _external=True)},
        {"loc": url_for("contact", _external=True)}
    ]
    return Response(
        render_template("sitemap.xml", pages=pages, products=products),
        mimetype="application/xml"
    )

# ---------- اجرای برنامه ----------
if __name__ == "__main__":
    app.run(debug=True)
