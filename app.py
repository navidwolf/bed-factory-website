from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# لیست محصولات (8 محصول)
products = [
    {"id": 1, "name": "تخت یک نفره", "price": 1500000, "image": "product1.webp", "tag": "جدید", "rating": 4.5},
    {"id": 2, "name": "تخت دو نفره", "price": 2500000, "image": "product2.webp", "tag": "تخفیف", "rating": 4.0},
    {"id": 3, "name": "تخت کودک", "price": 1200000, "image": "product3.webp", "tag": "جدید", "rating": 5.0},
    {"id": 4, "name": "تخت مهمان", "price": 1800000, "image": "product4.webp", "tag": "", "rating": 3.5},
    {"id": 5, "name": "تخت دو طبقه", "price": 3000000, "image": "product5.webp", "tag": "جدید", "rating": 4.0},
    {"id": 6, "name": "تخت سلطنتی", "price": 4500000, "image": "product6.webp", "tag": "تخفیف", "rating": 5.0},
    {"id": 7, "name": "تخت اسپرت", "price": 2200000, "image": "product7.webp", "tag": "", "rating": 4.5},
    {"id": 8, "name": "تخت راحتی", "price": 2000000, "image": "product8.webp", "tag": "جدید", "rating": 4.0}
]

# صفحه اصلی
@app.route('/')
def index():
    return render_template("index.html")

# صفحه محصولات
@app.route('/products')
def products_page():
    return render_template("products.html", products=products)

# صفحه جزئیات محصول
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return render_template("product_detail.html", product=product)

# صفحه سبد خرید
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total)

# افزودن محصول به سبد خرید
@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart_items = session.get('cart', [])
        cart_items.append(product)
        session['cart'] = cart_items
    return redirect(url_for('cart'))

# خالی کردن سبد خرید
@app.route('/clear-cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))

# صفحه پرداخت
@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template("checkout.html", cart_items=cart_items, total=total)

# صفحه تماس با ما
@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
