from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# مدل محصول
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    rating = db.Column(db.Float)
    tag = db.Column(db.String(50), nullable=True)
    short_description = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

# مدل کاربر admin
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

# صفحه اصلی
@app.route("/")
def index():
    products = Product.query.limit(4).all()
    return render_template("index.html", products=products)

# صفحه محصولات
@app.route("/products")
def products_page():
    products = Product.query.all()
    return render_template("products.html", products=products)

# جزئیات محصول
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

# صفحه تماس
@app.route("/contact")
def contact():
    return render_template("contact.html")

# صفحه سبد خرید
@app.route("/cart")
def cart():
    return render_template("cart.html")

# پنل مدیریت
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session["admin"] = admin.username
            return redirect(url_for("dashboard"))
    return render_template("admin/login.html")

@app.route("/admin/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    products = Product.query.all()
    return render_template("admin/dashboard.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
