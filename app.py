from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# تنظیم دیتابیس (SQLite)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# مدل محصول
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, default=0)
    short_description = db.Column(db.String(255))
    description = db.Column(db.Text)
    tag = db.Column(db.String(50))

# ساخت جداول و محصولات اولیه
@app.before_first_request
def init_db():
    db.create_all()
    if not Product.query.first():
        sample_products = [
            Product(name="تخت کلاسیک", price=4500000, image="product1.webp", rating=4.5, tag="جدید",
                    description="تخت کلاسیک با طراحی سنتی و کیفیت بالا."),
            Product(name="تخت مدرن", price=5200000, image="product2.webp", rating=4.8, tag="پرفروش",
                    description="تخت مدرن برای اتاق خواب‌های مینیمال."),
            Product(name="تخت دو نفره", price=6000000, image="product3.webp", rating=4.2,
                    description="تخت دو نفره مناسب برای زوج‌ها."),
            Product(name="تخت مینیمال", price=4800000, image="product4.webp", rating=4.7,
                    description="تخت مینیمال ساده و زیبا."),
            Product(name="تخت سلطنتی", price=7500000, image="product5.webp", rating=4.9, tag="جدید",
                    description="تخت سلطنتی لوکس و باشکوه."),
            Product(name="تخت نوجوان", price=3900000, image="product6.webp", rating=4.1,
                    description="تخت مناسب برای نوجوانان با طراحی شیک."),
            Product(name="تخت چوبی", price=5100000, image="product7.webp", rating=4.4,
                    description="تخت ساخته شده از چوب طبیعی."),
            Product(name="تخت راحتی", price=4300000, image="product8.webp", rating=4.3,
                    description="تخت راحتی برای خواب آسوده.")
        ]
        db.session.add_all(sample_products)
        db.session.commit()

# ----------------------
# روت‌های سایت اصلی
# ----------------------
@app.route("/")
def index():
    products = Product.query.limit(4).all()
    return render_template("index.html", products=products)

@app.route("/products")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ----------------------
# مدیریت سبد خرید (ساده)
# ----------------------
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get("cart", [])
    cart.append(product.id)
    session["cart"] = cart
    return redirect(url_for("cart"))

# ----------------------
# پنل مدیریت
# ----------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
    return render_template("admin/login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    products = Product.query.all()
    return render_template("admin/dashboard.html", products=products)

# ----------------------
# اجرای برنامه
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
