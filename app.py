from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# نمونه داده محصولات
products = [
    {'id': 1, 'name': 'تشک خوشخواب', 'price': 1200000},
    {'id': 2, 'name': 'بالش طبی', 'price': 250000},
    {'id': 3, 'name': 'ملحفه کتان', 'price': 300000},
]

# داده meta سایت
meta = {
    'site_name': 'فروشگاه تخت و تشک'
}

@app.route('/')
def home():
    return redirect(url_for('products_page'))

@app.route('/products')
def products_page():
    return render_template('products.html', products=products, meta=meta)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = []
    total_price = 0
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = next((p for p in products if p['id'] == int(product_id)), None)
            if product:
                subtotal = product['price'] * quantity
                cart_items.append({
                    'id': product['id'],
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total_price += subtotal
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, meta=meta)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'cart' not in session:
        session['cart'] = {}
    for product_id in list(session['cart'].keys()):
        new_qty = int(request.form.get(f'quantity_{product_id}', 1))
        if new_qty > 0:
            session['cart'][product_id] = new_qty
        else:
            session['cart'].pop(product_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and str(product_id) in session['cart']:
        session['cart'].pop(str(product_id))
        session.modified = True
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
