from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# =========================
# تنظیمات اصلی اپلیکیشن
# =========================
app = Flask(__name__)

# کلید امنیتی برای سشن‌ها
app.config['SECRET_KEY'] = "mysecretkey"

# مسیر دیتابیس (SQLite)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# مدل‌های دیتابیس
# =========================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Order {self.id} - {self.customer_name}>"

# =========================
# راه‌اندازی Flask-Admin
# =========================
admin = Admin(app, name="مدیریت سایت", template_mode="bootstrap3")
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Order, db.session))

# =========================
# مسیرهای عمومی سایت
# =========================
@app.route("/")
def index():
    products = Product.query.all()
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

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        total = request.form.get("total", 0)
        order = Order(customer_name=name, customer_email=email, total_price=total)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("checkout.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# =========================
# اجرای اپلیکیشن
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ساخت دیتابیس و جداول در اولین اجرا
    app.run(debug=True)
