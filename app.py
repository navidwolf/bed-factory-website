from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_session import Session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# تنظیمات برای ذخیره session روی فایل (یا می‌توانید روی سرور دیگری)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# داده‌های نمونه محصولات
products = [
    {"id": 1, "name": "تخت خواب 1", "price": 1000000, "description": "توضیحات تخت 1", "image": "product1.webp"},
    {"id": 2, "name": "تخت خواب 2", "price": 1200000, "description": "توضیحات تخت 2", "image": "product2.webp"},
    {"id": 3, "name": "تخت خواب 3", "price": 900000, "description": "توضیحات تخت 3", "image": "product3.webp"},
    {"id": 4, "name": "تخت خواب 4", "price": 1100000, "description": "توضیحات تخت 4", "image": "product4.webp"},
    {"id": 5, "name": "تخت خواب 5", "price": 950000, "description": "توضیحات تخت 5", "image": "product5.webp"},
    {"id": 6, "name": "تخت خواب 6", "price": 1300000, "description": "توضیحات تخت 6", "image": "product6.webp"},
    {"id": 7, "name": "تخت خواب 7", "price": 1250000, "description": "توضیحات تخت 7", "image": "product7.webp"},
    {"id": 8, "name": "تخت خواب 8", "price": 1400000, "description": "توضیحات تخت 8", "image": "product8.webp"},
]

# Context processor برای ارسال meta به تمام قالب‌ها
@app.context_processor
def inject_meta():
    return {
        "meta": {
            "site_name": "Bed Factory"
        }
    }

# صفحه اصلی
@app.route('/')
def home():
    return render_template('index.html')

# صفحه محصولات
@app.route('/products')
def products_page():
    return render_template('products.html', products=products)

# افزودن به سبد خرید با AJAX
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('id'))
    quantity = int(request.form.get('quantity', 1))

    # پیدا کردن محصول
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "محصول یافت نشد"}), 404

    # گرفتن سبد خرید از session
    cart = session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            "name": product["name"],
            "price": product["price"],
            "description": product["description"],
            "image": product["image"],
            "quantity": quantity
        }

    session['cart'] = cart
    session.modified = True

    return jsonify({"success": True, "cart": cart})

# حذف محصول از سبد خرید
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('id')
    cart = session.get('cart', {})

    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        session.modified = True
        return jsonify({"success": True, "cart": cart})
    return jsonify({"error": "محصول یافت نشد"}), 404

# به‌روزرسانی تعداد محصول در سبد خرید
@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('id')
    action = request.form.get('action')
    cart = session.get('cart', {})

    if product_id in cart:
        if action == "increase":
            cart[product_id]['quantity'] += 1
        elif action == "decrease" and cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1
        session['cart'] = cart
        session.modified = True
        return jsonify({"success": True, "cart": cart})
    return jsonify({"error": "محصول یافت نشد"}), 404

# صفحه سبد خرید
@app.route('/cart')
def cart_page():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

# صفحه پرداخت
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

# اجرای اپلیکیشن
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
