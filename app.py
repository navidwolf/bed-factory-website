import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# === ایجاد فولدر instance برای دیتابیس ===
os.makedirs("instance", exist_ok=True)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# === مدل دیتابیس ===
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Float, default=0)
    tag = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(200), nullable=True)

# === ساخت دیتابیس در صورت وجود نداشتن ===
with app.app_context():
    db.create_all()
    # افزودن محصولات نمونه اگر دیتابیس خالی باشد
    if Product.query.count() == 0:
        sample_products = [
            Product(name="تخت خوشخواب مدل A", price=2500000, image="bed1.jpg", rating=4.5, tag="پرفروش", short_description="تختی راحت و با کیفیت", description="این تخت مدل A کیفیت عالی دارد."),
            Product(name="تخت خوشخواب مدل B", price=3000000, image="bed2.jpg", rating=4.8, tag="جدید", short_description="تختی شیک و مدرن", description="این تخت مدل B مناسب فضاهای کوچک."),
        ]
        db.session.add_all(sample_products)
        db.session.commit()

# === نمونه سبد خرید ساده ===
cart_items = []

# === روت خانه ===
@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

# === روت محصولات ===
@app.route("/products")
def products_page():
    products = Product.query.all()
    return render_template("products.html", products=products)

# === روت جزئیات محصول ===
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

# === افزودن به سبد خرید ===
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_items.append(product)
    return redirect(url_for("cart"))

# === مشاهده سبد خرید ===
@app.route("/cart")
def cart():
    return render_template("cart.html", cart_items=cart_items)

# === پرداخت (نمونه) ===
@app.route("/checkout")
def checkout():
    cart_items.clear()
    return "<h2>پرداخت با موفقیت انجام شد!</h2>"

# === اجرا ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
