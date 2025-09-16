from flask import Flask, render_template, url_for, Response
from datetime import datetime

app = Flask(__name__)

# اطلاعات متا سایت
SITE_META = {
    'site_name': 'Bed Factory Co.',
    'description': 'تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.',
    'phone': '+98-21-12345678',
    'address': 'تهران، خیابان نمونه، نبش کارخانه',
    'email': 'info@bedfactory.example'
}

# Context processor برای ارسال متغیر now به همه قالب‌ها
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# صفحه اصلی
@app.route('/')
def index():
    products = [
        { 'id': 1, 'title': 'تخت خواب مدل آریا', 'image': url_for('static', filename='images/product1.webp'), 'excerpt': 'کلاف چوبی، راحتی بالا' },
        { 'id': 2, 'title': 'تخت خواب مدل نیلا', 'image': url_for('static', filename='images/product2.webp'), 'excerpt': 'مدرن و شیک' },
    ]
    return render_template('index.html', meta=SITE_META, products=products)

# صفحه محصولات
@app.route('/products')
def products():
    products_list = [
        { 
            'id': 1, 
            'title': 'تخت خواب مدل آریا', 
            'image': url_for('static', filename='images/product1.webp'), 
            'desc': 'کلاف چوبی استاندارد، ابعاد مختلف',
            'full_desc': 'تخت خواب مدل آریا با طراحی کلاسیک و راحتی بالا'
        },
        { 
            'id': 2, 
            'title': 'تخت خواب مدل نیلا', 
            'image': url_for('static', filename='images/product2.webp'), 
            'desc': 'مناسب فضاهای مدرن، قابل سفارش',
            'full_desc': 'تخت خواب مدل نیلا با طراحی مدرن و شیک'
        },
    ]
    return render_template('products.html', meta=SITE_META, products=products_list)

# صفحه تماس با ما
@app.route('/contact')
def contact():
    return render_template('contact.html', meta=SITE_META)

# جزئیات محصول
@app.route('/product/<int:id>')
def product_detail(id):
    products_dict = {
        1: {
            'title': 'تخت خواب مدل آریا',
            'image': url_for('static', filename='images/product1.webp'),
            'full_desc': 'تخت خواب مدل آریا با کلاف چوبی استاندارد، راحتی عالی و طراحی کلاسیک.'
        },
        2: {
            'title': 'تخت خواب مدل نیلا',
            'image': url_for('static', filename='images/product2.webp'),
            'full_desc': 'تخت خواب مدل نیلا با طراحی مدرن، رنگ‌بندی شیک و قابلیت سفارش سفارشی.'
        }
    }
    product = products_dict.get(id)
    if not product:
        return "محصول یافت نشد", 404
    return render_template('product_detail.html', meta=SITE_META, product=product)

# Route کامل و داینامیک برای sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    pages = []
    today = datetime.now().date().isoformat()

    # صفحات اصلی
    static_pages = ['index', 'products', 'contact']
    for page in static_pages:
        pages.append({
            'loc': url_for(page, _external=True),
            'lastmod': today
        })

    # محصولات داینامیک از همان dictionary
    products_dict = {
        1: 'تخت خواب مدل آریا',
        2: 'تخت خواب مدل نیلا'
    }
    for pid in products_dict.keys():
        pages.append({
            'loc': url_for('product_detail', id=pid, _external=True),
            'lastmod': today
        })

    # ساخت XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append('<url>')
        xml.append(f"<loc>{p['loc']}</loc>")
        xml.append(f"<lastmod>{p['lastmod']}</lastmod>")
        xml.append('</url>')
    xml.append('</urlset>')

    return Response('\n'.join(xml), mimetype='application/xml')

# اجرای برنامه
if __name__ == '__main__':
    app.run(debug=True)
