from flask import Flask, render_template, url_for
from datetime import datetime

app = Flask(__name__)

# اطلاعات سایت
SITE_META = {
    'site_name': 'کارخانه تخت خواب سازی ایرانیان',
    'author': 'Navid Wolf'
}

# محصولات نمونه
PRODUCTS = [
    {
        'id': 1,
        'name': 'تخت خواب مدل آریارو',
        'image': url_for('static', filename='images/product1.webp'),
        'description': 'تخت خوابی شیک و مدرن با طراحی منحصر به فرد.'
    },
    {
        'id': 2,
        'name': 'تخت خواب مدل نیلارو',
        'image': url_for('static', filename='images/product2.webp'),
        'description': 'تخت خوابی لوکس با استحکام بالا و طراحی جذاب.'
    }
]

# صفحه اصلی
@app.route('/')
def index():
    return render_template('index.html', meta=SITE_META, products=PRODUCTS, now=datetime.now())

# لیست محصولات
@app.route('/products')
def products():
    return render_template('products.html', meta=SITE_META, products=PRODUCTS, now=datetime.now())

# صفحه جزئیات محصول
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template('product_detail.html', meta=SITE_META, product=product, now=datetime.now())

# صفحه تماس با ما
@app.route('/contact')
def contact():
    return render_template('contact.html', meta=SITE_META, now=datetime.now())

if __name__ == '__main__':
    app.run(debug=True)
