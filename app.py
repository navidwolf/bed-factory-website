from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# محصولات ۸تایی
products = [
    {"id": 1, "name": "تخت خواب مدل A", "price": 200, "old_price": 250, "image": "product1.webp", "tag": "New", "rating": 5, "description": "توضیحات محصول ۱"},
    {"id": 2, "name": "تخت خواب مدل B", "price": 180, "old_price": 200, "image": "product2.webp", "tag": "Sale", "rating": 4, "description": "توضیحات محصول ۲"},
    {"id": 3, "name": "تخت خواب مدل C", "price": 220, "old_price": None, "image": "product3.webp", "tag": "New", "rating": 5, "description": "توضیحات محصول ۳"},
    {"id": 4, "name": "تخت خواب مدل D", "price": 210, "old_price": 230, "image": "product4.webp", "tag": "Sale", "rating": 4, "description": "توضیحات محصول ۴"},
    {"id": 5, "name": "تخت خواب مدل E", "price": 190, "old_price": None, "image": "product5.webp", "tag": "New", "rating": 5, "description": "توضیحات محصول ۵"},
    {"id": 6, "name": "تخت خواب مدل F", "price": 240, "old_price": 260, "image": "product6.webp", "tag": "Sale", "rating": 4, "description": "توضیحات محصول ۶"},
    {"id": 7, "name": "تخت خواب مدل G", "price": 230, "old_price": None, "image": "product7.webp", "tag": "New", "rating": 5, "description": "توضیحات محصول ۷"},
    {"id": 8, "name": "تخت خواب مدل H", "price": 250, "old_price": 280, "image": "product8.webp", "tag": "Sale", "rating": 4, "description": "توضیحات محصول ۸"}
]

# سبد خرید
def init_cart():
    if "cart" not in session:
        session["cart"] = []

def calculate_total():
    return sum(item["product"]["price"] * item["quantity"] for item in session.get("cart", []))

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/products")
def product_list():
    return render_template("products.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "محصول یافت نشد", 404
    return render_template("product_detail.html", product=product)

@app.route("/add-to-cart/<int:product_id>", methods=["GET", "POST"])
def add_to_cart(product_id):
    init_cart()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "محصول یافت نشد", 404
    quantity = int(request.form.get("quantity", 1))
    # بررسی اگر محصول قبلا اضافه شده
    for item in session["cart"]:
        if item["product"]["id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        session["cart"].append({"product": product, "quantity": quantity})
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/cart", methods=["GET", "POST"])
def cart():
    init_cart()
    total = calculate_total()
    return render_template("cart.html", cart=session["cart"], total=total)

@app.route("/update-cart/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    init_cart()
    quantity = int(request.form.get("quantity", 1))
    for item in session["cart"]:
        if item["product"]["id"] == product_id:
            item["quantity"] = quantity
            break
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    init_cart()
    if request.method == "POST":
        # پردازش سفارش (نمونه ساده)
        session.pop("cart", None)
        return "سفارش شما ثبت شد! با تشکر."
    return render_template("checkout.html")

if __name__ == "__main__":
    app.run(debug=True)
