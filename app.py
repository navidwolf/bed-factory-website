from flask import Flask, render_template, url_for, Response
from datetime import datetime

app = Flask(__name__)

# Basic site data — customize
SITE_META = {
    'site_name': 'Bed Factory Co.',
    'description': 'تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.',
    'phone': '+98-21-12345678',
    'address': 'تهران، خیابان نمونه، نبش کارخانه',
    'email': 'info@bedfactory.example'
}

@app.route('/')
def index():
    products = [
        { 'id': 1, 'title': 'تخت خواب مدل آریا', 'image': url_for('static', filename='images/product1.webp'), 'excerpt': 'کلاف چوبی، راحتی بالا' },
        { 'id': 2, 'title': 'تخت خواب مدل نیلا', 'image': url_for('static', filename='images/product2.webp'), 'excerpt': 'مدرن و شیک' },
    ]
    return render_template('index.html', meta=SITE_META, products=products)

@app.route('/products')
def products():
    products_list = [
        { 
            'id': 1, 
            'title': 'تخت خواب مدل آریا', 
            'image': url_for('static', filename='images/product1.webp'), 
            'desc': 'کلاف چوبی استاندارد، ابعاد مختلف',
            'full_desc': 'تخت خواب مدل آریا با استفاده از چوب با کیفیت ساخته شده است. مناسب برای اتاق‌های مدرن و راحت.'
        },
        { 
            'id': 2, 
            'title': 'تخت خواب مدل نیلا', 
            'image': url_for('static', filename='images/product2.webp'), 
            'desc': 'مناسب فضاهای مدرن، قابل سفارش',
            'full_desc': 'تخت خواب مدل نیلا با طراحی مدرن و شیک، مناسب فضاهای کوچک و بزرگ و قابل سفارش در ابعاد مختلف.'
        },
    ]
    return render_template('products.html', meta=SITE_META, products=products_list)

# مسیر جزئیات محصول
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    products_list = [
        { 
            'id': 1, 
            'title': 'تخت خواب مدل آریا', 
            'image': url_for('static', filename='images/product1.webp'), 
            'desc': 'کلاف چوبی استاندارد، ابعاد مختلف',
            'full_desc': 'تخت خواب مدل آریا با استفاده از چوب با کیفیت ساخته شده است. مناسب برای اتاق‌های مدرن و راحت.'
        },
        { 
            'id': 2, 
            'title': 'تخت خواب مدل نیلا', 
            'image': url_for('static', filename='images/product2.webp'), 
            'desc': 'مناسب فضاهای مدرن، قابل سفارش',
            'full_desc': 'تخت خواب مدل نیلا با طراحی مدرن و شیک_
