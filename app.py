from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# داده‌های نمونه
products = [
    {"id": 1, "name": "تخت خواب 1", "price": 1000},
    {"id": 2, "name": "تخت خواب 2", "price": 1500},
    {"id": 3, "name": "تخت خواب 3", "price": 2000},
]
messages = []

# ---------------------
# مسیرهای سایت اصلی
# ---------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products_page():
    return render_template("products.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    return render_template("product_detail.html", product=product)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        msg = request.form.get("message")
        messages.append({"id": len(messages)+1, "name": name, "email": email, "message": msg})
        flash("پیام شما ارسال شد!")
    return render_template("contact.html")

# ---------------------
# پنل ادمین
# ---------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "1234":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("نام کاربری یا رمز اشتباه است!")
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/admin")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return render_template("admin/dashboard.html", products=products, messages=messages)

@app.route("/admin/product/add", methods=["POST"])
def admin_add_product():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    name = request.form.get("name")
    price = request.form.get("price")
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    products.append({"id": new_id, "name": name, "price": price})
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/product/delete/<int:product_id>")
def admin_delete_product(product_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    global products
    products = [p for p in products if p["id"] != product_id]
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
