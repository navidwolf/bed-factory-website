from flask import Flask, render_template, url_for, Response, session, redirect, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # برای session

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
    1: {'title': 'تخت خواب مدل آریا', 'image': 'product1.webp','full_desc':'تخت خواب مدل آریا با طراحی کلاسیک و راحتی بالا'},
    2: {'title': 'تخت خواب مدل نیلا', 'image': 'product2.webp','full_desc':'تخت خواب مدل نیلا با طراحی مدرن و شیک'},
    3: {'title': 'تخت خواب مدل پارمیس', 'image': 'product3.webp','full_desc':'تخت خواب مدل پارمیس با طراحی مدرن و راحتی عالی'},
    4: {'title': 'تخت خواب مدل نیوشا', 'image': 'product4.webp','full_desc':'تخت خواب مدل نیوشا با طراحی کلاسیک و رنگ‌بندی شیک'},
    5: {'title': 'تخت خواب مدل ماهور', 'image': 'product5.webp','full_desc':'تخت خواب مدل ماهور با طراحی مدرن و راحتی بالا'},
    6: {'title': 'تخت خواب مدل یکتا', 'image': 'product6.webp','full_desc':'تخت خواب مدل یکتا با طراحی شیک و راحت'},
    7: {'title': 'تخت خواب مدل سولینا', 'image': 'product7.webp','full_desc':'تخت خواب مدل سولینا با طراحی زیبا و راحت'},
    8: {'title': 'تخت خواب مدل آرامیس', 'image': 'product8.webp','full_desc':'تخت خواب مدل آرامیس با طراحی شیک و مقاوم'}
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

# ===== سبد خرید =====
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    return redirect(url_for('cart'))  # وقتی دکمه کلیک شد وارد صفحه سبد خرید میشه

@app.route('/cart')
def cart():
    cart_items = []
    cart = session.get('cart', [])
    for pid in cart:
        product = products_dict.get(pid)
        if product:
            cart_items.append({
                'id': pid,
                'title': product['title'],
                'image': url_for('static', filename=f'images/{product["image"]}'),
                'full_desc': product['full_desc']
            })
    return render_template('cart.html', meta=SITE_META, cart=cart)

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)
        return "<h2>سفارش شما ثبت شد. ممنون!</h2>"
    return render_template('checkout.html', meta=SITE_META)

@app.route('/contact')
def contact():
    return render_template('contact.html', meta=SITE_META)

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    today = datetime.now().date().isoformat()
    static_pages = ['index','products','contact']
    for page in static_pages:
        pages.append({'loc': url_for(page, _external=True), 'lastmod': today})
    for pid in products_dict.keys():
        pages.append({'loc': url_for('product_detail', id=pid, _external=True), 'lastmod': today})

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append('<url>')
        xml.append(f"<loc>{p['loc']}</loc>")
        xml.append(f"<lastmod>{p['lastmod']}</lastmod>")
        xml.append('</url>')
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)
