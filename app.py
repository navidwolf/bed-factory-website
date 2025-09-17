from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "your_secret_key"

# نمونه محصولات
products = [
    {"id": 1, "name": "تخت خواب مدل 1", "price": 1500000, "description": "تخت دو نفره با کفی MDF", "image": "product1.webp"},
    {"id": 2, "name": "تخت خواب مدل 2", "price": 1200000, "description": "تخت یک نفره با کشو", "image": "product2.webp"},
    {"id": 3, "name": "تخت خواب مدل 3", "price": 2000000, "description": "تخت دو نفره لوکس با تاج چوبی", "image": "product3.webp"},
    {"id": 4, "name": "تخت خواب مدل 4", "price": 1700000, "description": "تخت یک نفره ساده", "image": "product4.webp"},
    {"id": 5, "name": "تخت خواب مدل 5", "price": 2500000, "description": "تخت دو نفره با کشو", "image": "product5.webp"},
    {"id": 6, "name": "تخت خواب مدل 6", "price": 1800000, "description": "تخت یک نفره با تاج چوبی", "image": "product6.webp"},
    {"id": 7, "name": "تخت خواب مدل 7", "price": 3000000, "description": "تخت دو نفره لوکس با MDF", "image": "product7.webp"},
    {"id": 8, "name": "تخت خواب مدل 8", "price": 2200000, "description": "تخت دو نفره ساده", "image": "product8.webp"},
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products_page():
    return render_template('products.html', products=products)

@app.route('/cart')
def cart_page():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/add_to_cart_ajax/<int:product_id>', methods=['POST'])
def add_to_cart_ajax(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            "name": product['name'],
            "price": product['price'],
            "description": product['description'],
            "image": product['image'],
            "quantity": 1
        }

    session['cart'] = cart
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    total_items = sum(item['quantity'] for item in cart.values())
    return jsonify({"cart": cart, "total": total, "total_items": total_items})

@app.route('/update_cart_ajax', methods=['POST'])
def update_cart_ajax():
    data = request.get_json()
    product_id = str(data.get("product_id"))
    action = data.get("action")
    
    cart = session.get('cart', {})
    if product_id in cart:
        if action == "increase":
            cart[product_id]['quantity'] += 1
        elif action == "decrease":
            cart[product_id]['quantity'] -= 1
            if cart[product_id]['quantity'] <= 0:
                cart.pop(product_id)
        elif action == "remove":
            cart.pop(product_id)
    session['cart'] = cart

    total = sum(item['price'] * item['quantity'] for item in cart.values())
    total_items = sum(item['quantity'] for item in cart.values())
    return jsonify(cart=cart, total=total, total_items=total_items)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

if __name__ == "__main__":
    app.run(debug=True)
