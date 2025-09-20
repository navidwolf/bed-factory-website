from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# مسیر مطلق دیتابیس
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "instance", "database.db")
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# مدل ادمین
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# مدل محصول
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

# صفحه ورود ادمین
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session["admin"] = admin.username
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid credentials"
    return render_template("admin/login.html")

# داشبورد ادمین
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    products = Product.query.all()
    return render_template("admin/dashboard.html", products=products)

# افزودن محصول
@app.route("/admin/products/add", methods=["GET", "POST"])
def add_product():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        new_product = Product(name=name, price=float(price))
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/add_product.html")

# ویرایش محصول
@app.route("/admin/products/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = float(request.form["price"])
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_product.html", product=product)

# حذف محصول
@app.route("/admin/products/delete/<int:id>")
def delete_product(id):
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

# صفحه اصلی
@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
