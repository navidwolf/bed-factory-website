from flask import Flask, render_template, session, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# نمونه محصولات
products = [
    {"id": 1, "title": "تخت خواب مدل آریا", "excerpt": "کلاس چوبی، راحتی بالا", "full_desc": "توضیح کامل تخت خواب آریا ...", "image": "/static/images/product1.webp", "price": 2500000},
    {"id": 2, "title": "تخت خواب مدل نیلا", "excerpt": "مدرن و شیک", "full_desc": "توضیح کامل تخت خواب نیلا ...", "image": "/static/images/product2.webp", "price": 2800000},
    {"id": 3, "title": "تخت خواب مدل پارمیس", "excerpt": "چوب با کیفیت، راحت", "full_desc": "توضیح کامل تخت خواب پارمیس ...", "image": "/static/images/product3.webp", "price": 3000000},
    {"id": 4, "title": "تخت خواب مدل نیوشا", "excerpt": "شیک و محکم", "full_desc": "توضیح کامل تخت خواب نیوشا ...", "image": "/static/images/product4.webp", "price": 2700000},
    {"id": 5, "title": "تخت خواب مدل سارا", "excerpt": "مدرن و راحت", "full_desc": "توضیح کامل تخت خواب سارا ...", "image": "/static/images/product5.webp", "price": 2600000},
    {"id": 6, "title": "تخت خواب مدل نسترن", "excerpt": "زیبا و مقاوم", "full_desc": "توضیح کامل تخت خواب نسترن ...", "image": "/static/images/product6.webp", "price": 3200000},
    {"id": 7, "title": "تخت خواب مدل مهسا", "excerpt": "شیک و بادوام", "full_desc": "توضیح کامل تخت خواب مهسا ...", "image": "/static/images/product7.webp", "price": 2400000},
    {"id": 8, "title": "تخت خواب مدل باران", "excerpt": "سبک و زیبا", "full_desc": "توضیح کامل تخت خواب باران ...", "image": "/static/images/product8.webp", "price": 2300000},
]

# دیکشنری برای دسترسی سریع
products_dict = {p["id"]: p for p in products}

# -------------------------
# صفحات
# -------------------------
@app.route("/")
def index():
    return render_template("index.html", products=products[:4])

@app.route("/products")
def products_page():
    return render_template("products.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = products_dict.get(product_id)
    if not product:
        return "محصول یافت نشد", 404
    return render_template("product_detail.html", product=product)

@app.route("/contact")
def contact():
    return render_template("contact.html")

# -------------------------
# سبد خرید
# -------------------------
@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = products_dict.get(pid)
        if product:
            subtotal = product["price"] * qty
            items.append({"product": product, "qty": qty, "subtotal": subtotal})
            total += subtotal
    return render_template("cart.html", items=items, total=total)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    try:
        product_id = int(request.form.get("product_id", 0))
    except (TypeError, ValueError):
        return redirect(url_for("products_page"))

    if product_id not in products_dict:
        return "محصول یافت نشد", 404

    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart"))

# -------------------------
# شمارش سبد خرید برای هدر
# -------------------------
@app.context_processor
def inject_now_and_cartcount():
    cart = session.get("cart", {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return {"now": datetime.now(), "cart_count": cart_count}
