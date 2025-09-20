from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bed_factory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# مدل محصول
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=5.0)
    short_description = db.Column(db.String(200))
    description = db.Column(db.Text)
    tag = db.Column(db.String(50))

# صفحه اصلی
@app.route('/')
def index():
    products = Product.query.limit(8).all()
    return render_template('index.html', products=products)

# صفحه محصولات
@app.route('/products')
def products_page():
    products = Product.query.all()
    return render_template('products.html', products=products)

# جزئیات محصول
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# صفحه تماس با ما
@app.route('/contact')
def contact():
    return render_template('contact.html')

# صفحه سبد خرید (نمونه)
@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)
