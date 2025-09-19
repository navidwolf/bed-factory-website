from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# دیتابیس
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# مدل‌ها
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 🛒 سبد خرید
def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart
    session.modified = True

# صفحات اصلی
@app.route('/')
def index():
    products = Product.query.limit(4).all()
    return render_template('index.html', products=products)

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
@login_required
def cart():
    cart = get_cart()
    product_ids = list(cart.keys())
    products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []
    return render_template('cart.html', cart=cart, products=products)

@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    save_cart(cart)
    flash("محصول به سبد اضافه شد.", "success")
    return redirect(request.referrer or url_for('products'))

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = get_cart()
    if str(product_id) in cart:
        del cart[str(product_id)]
        save_cart(cart)
    flash("محصول از سبد حذف شد.", "warning")
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

# فرم تماس
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        flash("پیام شما با موفقیت ارسال شد!", "success")
        return render_template('contact.html', success=True)
    return render_template('contact.html')

# ثبت‌نام و ورود
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("نام کاربری موجود است.", "danger")
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("ثبت‌نام با موفقیت انجام شد. لطفاً وارد شوید.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("ورود موفق!", "success")
            return redirect(url_for('index'))
        flash("نام کاربری یا رمز اشتباه است.", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("خروج انجام شد.", "info")
    return redirect(url_for('index'))

# پنل مدیریت محصولات
@app.route('/admin')
@login_required
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image = request.form['image']
        product = Product(name=name, description=description, price=price, image=image)
        db.session.add(product)
        db.session.commit()
        flash("محصول با موفقیت اضافه شد!", "success")
        return redirect(url_for('admin'))
    return render_template('product_form.html', action="افزودن")

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.image = request.form['image']
        db.session.commit()
        flash("محصول با موفقیت ویرایش شد!", "success")
        return redirect(url_for('admin'))
    return render_template('product_form.html', product=product, action="ویرایش")

@app.route('/admin/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("محصول حذف شد!", "warning")
    return redirect(url_for('admin'))

# دیتابیس و محصولات اولیه
@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    products = [
        Product(name="تخت خواب ۱", description="تخت مدرن با کیفیت بالا", price=5_000_000, image="product1.webp"),
        Product(name="تخت خواب ۲", description="طراحی کلاسیک و زیبا", price=6_200_000, image="product2.webp"),
        Product(name="تخت خواب ۳", description="مناسب اتاق‌های کوچک", price=4_800_000, image="product3.webp"),
        Product(name="تخت خواب ۴", description="چوبی و مقاوم", price=7_500_000, image="product4.webp"),
        Product(name="تخت خواب ۵", description="دو نفره با طراحی خاص", price=8_000_000, image="product5.webp"),
        Product(name="تخت خواب ۶", description="مدرن و راحت", price=5_500_000, image="product6.webp"),
        Product(name="تخت خواب ۷", description="ساده و شیک", price=4_200_000, image="product7.webp"),
        Product(name="تخت خواب ۸", description="لوکس و لاکچری", price=9_300_000, image="product8.webp"),
    ]
    db.session.add_all(products)
    db.session.commit()
    print("✅ دیتابیس ساخته شد و ۸ محصول اضافه شد.")

if __name__ == '__main__':
    app.run(debug=True)
