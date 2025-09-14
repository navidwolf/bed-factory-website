from flask import Flask, render_template, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from models import db, Product, SiteMeta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db.init_app(app)

# Admin panel
admin = Admin(app, name='مدیریت سایت', template_mode='bootstrap4')
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(SiteMeta, db.session))

# Initialize DB
with app.app_context():
    db.create_all()
    # اگر دیتای اولیه لازم داری، می‌توان اضافه کرد:
    if SiteMeta.query.count() == 0:
        meta = SiteMeta(
            site_name='Bed Factory Co.',
            description='تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.',
            phone='+98-21-12345678',
            address='تهران، خیابان نمونه، نبش کارخانه',
            email='info@bedfactory.example'
        )
        db.session.add(meta)
        db.session.commit()

@app.route('/')
def index():
    products = Product.query.all()
    meta = SiteMeta.query.first()
    return render_template('index.html', meta=meta, products=products)

@app.route('/products')
def products_page():
    products_list = Product.query.all()
    meta = SiteMeta.query.first()
    return render_template('products.html', meta=meta, products=products_list)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    meta = SiteMeta.query.first()
    return render_template('product_detail.html', meta=meta, product=product)

@app.route('/contact')
def contact():
    meta = SiteMeta.query.first()
    return render_template('contact.html', meta=meta)

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    today = datetime.now().date().isoformat()
    pages.append({'loc': url_for('index', _external=True), 'lastmod': today})
    pages.append({'loc': url_for('products_page', _external=True), 'lastmod': today})
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
