from flask import Flask, render_template, url_for, Response
from datetime import datetime

app = Flask(__name__)

# اطلاعات پایه سایت
SITE_META = {
    'site_name': 'کارخانه تخت خواب سازی ایرانیان',
    'description': 'تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.',
    'phone': '+98-21-12345678',
    'address': 'تهران، خیابان نمونه، نبش کارخانه',
    'email': 'info@bedfactory.example'
}

# محصولات
PRODUCTS = [
    {
        'id': 1,
        'title': 'تخت خواب مدل آریا',
        'image': url_for('static', filename='images/product1.webp'),
        'excerpt': 'کلاف چوبی، راحتی بالا',
        'desc': 'کلاف چوبی استاندارد، ابعاد مختلف',
        'full_desc': 'تخت خواب مدل آریا با طراحی کلاسیک، راحتی بالا و دوام عالی.'
    },
    {
        'id': 2,
        'title': 'تخت خواب مدل نیلا',
        'image': url_for('static', filename='images/product2.webp'),
        'excerpt': 'مدرن و شیک',
        'desc': 'مناسب فضاهای مدرن، قابل سفارش',
        'full_desc': 'تخت خواب مدل نیلا با طراحی مدرن، شیک و کاملاً مناسب اتاق‌های امروزی.'
    }
]

@app.route('/')
def index():
    return render_template('index.html', meta=SITE_META, products=PRODUCTS, now=datetime.now())

@app.route('/products')
def products():
    return render_template('products.html', meta=SITE_META, products=PRODUCTS, now=datetime.now())

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "محصول یافت نشد", 404
    return render_template('product_detail.html', meta=SITE_META, product=product, now=datetime.now())

@app.route('/contact')
def contact():
    return render_template('contact.html', meta=SITE_META, now=datetime.now())

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    today = datetime.now().date().isoformat()
    pages.append({'loc': url_for('index', _external=True), 'lastmod': today})
    pages.append({'loc': url_for('products', _external=True), 'lastmod': today})
    pages.append({'loc': url_for('contact', _external=True), 'lastmod': today})

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
