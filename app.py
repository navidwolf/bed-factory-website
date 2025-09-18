from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "secret123"

# محصولات نمونه
products = [
    {"id": 1, "name": "تشک رویال", "image": "product1.webp", "price": 3500000, "old_price": 4000000, "discount": 12, "is_new": False, "rating": 5, "description":"تشک راحت و بادوام"},
    {"id": 2, "name": "بالش طبی", "image": "product2.webp", "price": 500000, "old_price": 600000, "discount": 15, "is_new": False, "rating": 4, "description":"بالش طبی با حفظ ستون فقرات"},
    {"id": 3, "name": "پتو نرم", "image": "product3.webp", "price": 750000, "old_price": 900000, "discount": 17, "is_new": False, "rating": 5, "description":"پتو نرم و سبک برای خواب راحت"},
    {"id": 4, "name": "تشک کودک", "image": "product4.webp", "price": 2500000, "old_price": 2800000, "discount": 11, "is_new": True, "rating": 4, "description":"تشک کودک با بهترین مواد"},
    {"id": 5, "name": "کوسن تزئینی", "image": "product5.webp", "price": 350000, "old_price": 400000, "discount": 12, "is_new": True, "rating": 3, "description":"کوسن زیبا و نرم برای دکوراسیون"},
    {"id": 6, "name": "روبالشی", "image": "product6.webp", "price": 180000, "old_price": 200000, "discount": 10, "is_new": False, "rating": 4, "description":"روبالشی ضد حساسیت"},
    {"id": 7, "name": "ملحفه", "image": "product7.webp", "price": 900000, "old_price": 1100000, "discount": 18, "is_new": False, "rating": 5, "description":"ملحفه نرم و لطیف"},
    {"id": 8, "name": "تشک دونفره", "image": "product8.webp", "price": 5000000, "old_price": 5500000, "discount": 9, "is_new": True, "rating": 5, "description":"تشک دو نفره راحت و شیک"}
]

# سبد خرید در session
def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart

# صفحه اصلی
@app.route("/")
def index():
    return render_template("index.html", products=products)

# لیست همه محصولات
@app.route("/products")
def product_list():
    return render_template("products.html", products=products)

# جزئیات محصول
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "محصول یافت نشد", 404
    return render_template("product_detail.html", product=product, products=products)

# افزودن به سبد خرید
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    save_cart(cart)
    return redirect(request.referrer or url_for("index"))

# حذف از سبد خرید
@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)
    return redirect(url_for("cart"))

# صفحه سبد خرید
@app.route("/cart")
def cart():
    cart = get_cart()
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            cart_items.append({"product": product, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", cart_items=cart_items, total=total)

# صفحه پرداخت
@app.route("/checkout", methods=["GET","POST"])
def checkout():
    success = False
    if request.method == "POST":
        # اینجا می‌توان اطلاعات پرداخت را پردازش کرد
        session.pop("cart", None)
        success = True
    return render_template("checkout.html", success=success)
    
if __name__ == "__main__":
    app.run(debug=True)
