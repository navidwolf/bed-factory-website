from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
    UserMixin,
)
import os

# -------------------
# تنظیمات اصلی
# -------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/database.db"
app.config["SECRET_KEY"] = "your_secret_key_here"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# -------------------
# مدل‌ها
# -------------------
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(200), nullable=True)  # توضیح کوتاه
    image = db.Column(db.String(200), nullable=True)  # مسیر عکس
    tag = db.Column(db.String(50), nullable=True)  # برچسب مثل "جدید"
    rating = db.Column(db.Float, default=0)  # امتیاز


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# -------------------
# صفحات عمومی
# -------------------
@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/products")
def products_page():
    products = Product.query.all()
    return render_template("products.html", products=products)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)


@app.route("/contact")
def contact():
    return render_template("contact.html")


# -------------------
# مدیریت سبد خرید
# -------------------
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product_id)
    session.modified = True

    flash(f"{product.name} به سبد خرید اضافه شد.", "success")
    return redirect(url_for("products_page"))


@app.route("/cart")
def cart():
    cart_items = []
    if "cart" in session:
        cart_ids = session["cart"]
        cart_items = Product.query.filter(Product.id.in_(cart_ids)).all()
    return render_template("cart.html", cart_items=cart_items)


@app.route("/checkout")
def checkout():
    if "cart" not in session or len(session["cart"]) == 0:
        flash("سبد خرید شما خالی است.", "warning")
        return redirect(url_for("cart"))

    cart_ids = session["cart"]
    cart_items = Product.query.filter(Product.id.in_(cart_ids)).all()
    total_price = sum([p.price for p in cart_items])

    # خالی کردن سبد خرید بعد از پرداخت فرضی
    session.pop("cart", None)

    return render_template(
        "checkout.html", cart_items=cart_items, total_price=total_price
    )


# -------------------
# مدیریت (ادمین)
# -------------------
@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()
        if admin and bcrypt.check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for("dashboard"))
        else:
            flash("نام کاربری یا رمز عبور اشتباه است.", "danger")

    return render_template("admin/login.html")


@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/admin/dashboard")
@login_required
def dashboard():
    products = Product.query.all()
    return render_template("admin/dashboard.html", products=products)


@app.route("/admin/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        description = request.form.get("description")
        short_description = request.form.get("short_description")
        image = request.form.get("image")
        tag = request.form.get("tag")
        rating = float(request.form.get("rating", 0))

        product = Product(
            name=name,
            price=price,
            description=description,
            short_description=short_description,
            image=image,
            tag=tag,
            rating=rating,
        )
        db.session.add(product)
        db.session.commit()
        flash("محصول اضافه شد.", "success")
        return redirect(url_for("dashboard"))

    return render_template("admin/add_product.html")


@app.route("/admin/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.price = float(request.form["price"])
        product.description = request.form.get("description")
        product.short_description = request.form.get("short_description")
        product.image = request.form.get("image")
        product.tag = request.form.get("tag")
        product.rating = float(request.form.get("rating", 0))

        db.session.commit()
        flash("محصول ویرایش شد.", "success")
        return redirect(url_for("dashboard"))

    return render_template("admin/edit_product.html", product=product)


@app.route("/admin/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("محصول حذف شد.", "success")
    return redirect(url_for("dashboard"))


# -------------------
# اجرای برنامه
# -------------------
if __name__ == "__main__":
    os.makedirs("instance", exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
