from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# محصولات
products = [
    {"id": 1, "name": "تخت خواب مدل A", "price": 1200000, "image": "product1.webp", "tag": "جدید", "rating": 4},
    {"id": 2, "name": "تخت خواب مدل B", "price": 1500000, "image": "product2.webp", "tag": "تخفیف", "rating": 5},
    {"id": 3, "name": "تخت خواب مدل C", "price": 1000000, "image": "product3.webp", "tag": "جدید", "rating": 3},
    {"id": 4, "name": "تخت خواب مدل D", "price": 1700000, "image": "product4.webp", "tag": "تخفیف", "rating": 5},
    {"id": 5, "name": "تخت خواب مدل E", "price": 1300000, "image": "product5.webp", "tag": "جدید", "rating": 4},
    {"id": 6, "name": "تخت خواب مدل F", "price": 1600000, "image": "product6.webp", "tag": "تخفیف", "rating": 5},
    {"id": 7, "name": "تخت خواب مدل G", "price": 1400000, "image": "product7.webp", "tag": "جدید", "rating": 4},
    {"id": 8, "name": "تخت خواب مدل H", "price": 1800000, "image": "product8.webp", "tag": "تخفیف", "rating": 5},
]

# صفحه اصلی
@app.route("/")
def index():
    return render_template("index.html", products=products)

# فروشگاه
@app.route("/products")
def products_page():
    return render_template("products.html", products=products)

# جزئیات محصول
@app.route("/product/<int:id>")
def product_detail(id):
    product = next((p for p in products if p["id"] == id), None)
    return render_template("product_detail.html", product=product)

# سبد خرید
@app.route("/cart")
def cart():
    if "cart" not in session:
        session["cart"] = {}
    cart_items = []
    total = 0
    for pid, qty in session["cart"].items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            product_total = product["price"] * qty
            total += product_total
            cart_items.append({"product": product, "quantity": qty, "total": product_total})
    return render_template("cart.html", cart_items=cart_items, total=total)

# افزودن به سبد خرید
@app.route("/add-to-cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = {}
    session["cart"][str(id)] = session["cart"].get(str(id), 0) + 1
    session.modified = True
    return redirect(url_for("cart"))

# حذف از سبد خرید
@app.route("/remove-from-cart/<int:id>")
def remove_from_cart(id):
    if "cart" in session and str(id) in session["cart"]:
        session["cart"].pop(str(id))
        session.modified = True
    return redirect(url_for("cart"))

# صفحه پرداخت
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        session.pop("cart", None)
        return redirect(url_for("index"))
    if "cart" not in session:
        session["cart"] = {}
    cart_items = []
    total = 0
    for pid, qty in session["cart"].items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            product_total = product["price"] * qty
            total += product_total
            cart_items.append({"product": product, "quantity": qty, "total": product_total})
    return render_template("checkout.html", cart_items=cart_items, total=total)

# تماس با ما
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        print(f"پیام جدید از {name} ({email}): {message}")
        return redirect(url_for("contact"))
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
