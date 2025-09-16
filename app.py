from flask import Flask, render_template, url_for, Response, session, redirect, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

SITE_META = {
    'site_name': 'Bed Factory Co.',
    'description': 'تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.',
    'phone': '+98-21-12345678',
    'address': 'تهران، خیابان نمونه، نبش کارخانه',
    'email': 'info@bedfactory.example'
}

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

products_dict = {
    1: {'title': 'تخت خواب مدل آریا', 'image': 'product1.webp','excerpt':'کلاف چوبی، راحتی بالا','desc':'کلاف چوبی استاندارد، ابعاد مختلف','full_desc':'تخت خواب مدل آریا با طراحی کلاسیک و راحتی بالا','price': 2500000},
    2: {'title': 'تخت خواب مدل نیلا', 'image': 'product2.webp','excerpt':'مدرن و شیک','desc':'مناسب فضاهای مدرن، قابل سفارش','full_desc':'تخت خواب مدل نیلا با طراحی مدرن و شیک','price': 3000000},
    3: {'title': 'تخت خواب مدل پارمیس', 'image': 'product3.webp','excerpt':'چوب با کیفیت، راحت','desc':'ابعاد مختلف و طراحی زیبا','full_desc':'تخت خواب مدل پارمیس با طراحی مدرن و راحتی عالی','price': 2800000},
    4: {'title': 'تخت خواب مدل نیوشا', 'image': 'product4.webp','excerpt':'شیک و محکم','desc':'کلاف چوبی و قابلیت سفارش','full_desc':'تخت خواب مدل نیوشا با طراحی کلاسیک و رنگ‌بندی شیک','price': 3200000},
    5: {'title': 'تخت خواب مدل ماهور', 'image': 'product5.webp','excerpt':'راحت و مدرن','desc':'ابعاد استاندارد و قابل تنظیم','full_desc':'تخت خواب مدل ماهور با طراحی مدرن و راحتی بالا','price': 2900000},
    6: {'title': 'تخت خواب مدل یکتا', 'image': 'product6.webp','excerpt':'کیفیت عالی','desc':'چوب با دوام و طراحی زیبا','full_desc':'تخت خواب مدل یکتا با طراحی شیک و راحت','price': 3500000}
}

@app.route('/')
def index():
    products = []
    for pid, p in products_dict.items():
        prod = p.copy()
        prod['id'] = pid
        prod['image'] = url_for('static', filename=f'images/{p["image"]}')
        products.append(prod)
    return render_template('index.html', meta=SITE_META, products=products)

@app.route('/products')
def products():
    products = []
    for pid, p in products_dict.items():
        prod = p.copy()
        prod['id'] = pid
        prod['image'] = url_for('static', filename=f'images/{p["image"]}')
        products.append(prod)
    return render_template('products.html', meta=SITE_META, products=products)

@app.route('/product/<int:id>')
def product_detail(id):
    product = products_dict.get(id)
    if not product:
        return "محصول یافت نشد", 404
    prod = product.copy()
    prod['id'] = id
    prod['image'] = url_for('static', filename=f'images/{product["image"]}')
    return render_template('product_detail.html', meta=SITE_META, product=prod)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = []
    cart = session.get('cart', {})
    for pid, qty in cart.items():
        product = products_dict.get(pid)
        if product:
            cart_items.append({
                'id': pid,
                'title': product['title'],
                'price': product['price'],
                'quantity': qty,
                'total': product['price'] * qty
            })
    total_price = sum(item['total'] for item in cart_items)
    return render_template('cart.html', meta=SITE_META, cart=cart_items, total_price=total_price)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if session.get('cart'):
        if request.method == 'POST':
            session.pop('cart')
            return "<h2>سفارش شما ثبت شد. ممنون!</h2>"
        return render_template('checkout.html', meta=SITE_META)
    else:
        return redirect(url_for('cart'))

@app.route('/contact')
def contact():
    return render_template('contact.html', meta=SITE_META)

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    today = datetime.now().date().isoformat()
    static_pages = ['index', 'products', 'contact']
    for page in static_pages:
        pages.append({'loc': url_for(page, _external=True), 'lastmod': today})
    for pid in products_dict.keys():
        pages.append({'loc': url_for('product_detail', id=pid, _external=True), 'lastmod': today})
    xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append('<url>')
        xml.append(f"<loc>{p['loc']}</loc>")
        xml.append(f"<lastmod>{p['lastmod']}</lastmod>")
        xml.append('</url>')
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)
