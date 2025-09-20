from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

# مدل‌ها
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    rating = db.Column(db.Float)
    short_description = db.Column(db.String(200))
    description = db.Column(db.Text)
    tag = db.Column(db.String(50))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    customer_email = db.Column(db.String(100))
    status = db.Column(db.String(20), default="جدید")
    total_price = db.Column(db.Integer)


# --- مسیرهای سایت اصلی ---
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

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


# --- مدیریت سبد خرید (ساده) ---
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get("cart", [])
    cart.append({"id": product.id, "name": product.name, "price": product.price})
    session["cart"] = cart
    flash("محصول به سبد اضافه شد!", "success")
    return redirect(url_for("products"))


# --- مسیرهای پنل مدیریت ---
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("نام کاربری یا رمز اشتباه است", "danger")
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    product_count = Product.query.count()
    order_count = Order.query.count()
    return render_template("admin/dashboard.html", product_count=product_count, order_count=order_count)

# مدیریت محصولات
@app.route("/admin/products")
def admin_products():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    products = Product.query.all()
    return render_template("admin/products.html", products=products)

@app.route("/admin/products/add", methods=["GET", "POST"])
def admin_add_product():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        product = Product(
            name=request.form["name"],
            price=request.form["price"],
            image=request.form["image"],
            rating=request.form.get("rating", 0),
            short_description=request.form["short_description"],
            description=request.form["description"],
            tag=request.form["tag"]
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("admin_products"))
    return render_template("admin/add_product.html")

@app.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
def admin_edit_product(product_id):
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = request.form["price"]
        product.image = request.form["image"]
        product.rating = request.form.get("rating", 0)
        product.short_description = request.form["short_description"]
        product.description = request.form["description"]
        product.tag = request.form["tag"]
        db.session.commit()
        return redirect(url_for("admin_products"))
    return render_template("admin/edit_product.html", product=product)

@app.route("/admin/products/delete/<int:product_id>")
def admin_delete_product(product_id):
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("admin_products"))

# مدیریت سفارش‌ها
@app.route("/admin/orders")
def admin_orders():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    orders = Order.query.all()
    return render_template("admin/orders.html", orders=orders)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
