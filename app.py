from flask import Flask, render_template, url_for, Response, session, redirect
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key"  # برای مدیریت سبد خرید لازم است

# متای عمومی سایت
SITE_META = {
    "site_name": "Bed Factory Co.",
    "description": "تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.",
    "phone": "+98-21-12345678",
    "address": "تهران، خیابان نمونه، نبش کارخانه",
    "email": "info@bedfactory.example"
}

# Context processor برای ارسال متغیر now به همه قالب‌ها
@app.context_processor
def inject_now():
    return {"now": datetime.now()}

# محصولات
products = [
    { "id": 1, "title": "تخت خواب مدل آریا", "image": url_for('static', filename='images/product1.webp'),
      "excerpt": "کلاف چوبی، راحتی بالا", "desc": "کلاف چوبی استاندارد، ابعاد مختلف",
      "full_desc": "تخت خواب مدل آریا با طراحی کلاسیک و راحتی بالا" },

    { "id": 2, "title": "تخت خواب مدل نیلا", "image": url_for('static', filename='images/product2.webp'),
      "excerpt": "مدرن و شیک", "desc": "مناسب فضاهای مدرن، قابل سفارش",
      "full_desc": "تخت خواب مدل نیلا با طراحی مدرن و شیک" },

    { "id": 3, "title": "تخت خواب مدل پارمیس", "image": url_for('static', filename='images/product3.webp'),
      "excerpt": "مدرن و راحت", "desc": "دارای روکش چرم مصنوعی",
      "full_desc": "تخت خواب مدل پارمیس مناسب برای دکوراسیون مدرن و مینیمال" },

    { "id": 4, "title": "تخت خواب مدل سپنتا", "image": url_for('static', filename='images/product4.webp'),
      "excerpt": "چوب طبیعی", "desc": "استحکام بالا و طراحی لوکس",
      "full_desc": "تخت خواب مدل سپنتا ساخته‌شده از چوب طبیعی و مقاوم" },

    { "id": 5, "title": "تخت خواب مدل پرنس", "image": url_for('static', filename='images/product5.webp'),
      "excerpt": "طراحی سلطنتی", "desc": "لوکس و خاص",
      "full_desc": "تخت خواب مدل پرنس با طراحی کلاسیک سلطنتی برای خانه‌های لوکس" },

    { "id": 6, "title": "تخت خواب مدل مهتاب", "image": url_for('static', filename='images/product6.webp'),
      "excerpt": "سبک و ساده", "desc": "برای آپارتمان‌های کوچک",
      "full_desc": "تخت خواب مدل مهتاب مناسب برای اتاق‌های جمع و جور و آپارتمانی" },

    { "id": 7, "title": "تخت خواب مدل رویا", "image": url_for('static', filename='images/product7.webp'),
      "excerpt": "راحتی بی‌نظیر", "desc": "دارای تشک ارتوپدی",
      "full_desc": "تخت خواب مدل رویا برای کسانی که به سلامت خواب اهمیت می‌دهند" },

    { "id": 8, "title": "تخت خواب مدل ستاره", "image": url_for('static', filename='images/product8.webp'),
      "excerpt": "طراحی مدرن", "desc": "ترکیب فلز و چوب",
      "full_desc": "تخت خواب مدل ستاره ترکیبی زیبا از فلز و چوب برای دکوراسیون خاص" }
]

@app.route("/")
def index():
    return render_template("index.html", meta=SITE_META, products=products[:4])  # فقط ۴ محصول ویژه در صفحه اصلی

@app.route("/products")
def products_page():
    return render_template("products.html", meta=SITE_META, products=products)  # همه ۸ محصول در صفحه محصولات

@app.route("/contact")
def contact():
    return render_template("contact.html", meta=SITE_META)

@app.route("/product/<int:id>")
def product_detail(id):
    product = next((p for p in products if p["id"] == id), None)
    if not product:
        return "محصول یافت نشد", 404
    return render_template("product_detail.html", meta=SITE_META, product=product)

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", meta=SITE_META, cart=cart_items)

@app.route("/add-to-cart/<int:id>")
def add_to_cart(id):
    cart_items = session.get("cart", [])
    product = next((p for p in products if p["id"] == id), None)
    if product:
        cart_items.append(product)
        session["cart"] = cart_items
    return redirect("/cart")

@app.route("/sitemap.xml")
def sitemap():
    pages = []
    today = datetime.now().date().isoformat()
    pages.append({"loc": url_for("index", _external=True), "lastmod": today})
    pages.append({"loc": url_for("products_page", _external=True), "lastmod": today})
    pages.append({"loc": url_for("contact", _external=True), "lastmod": today})

    # اضافه کردن محصولات
    for p in products:
        pages.append({"loc": url_for("product_detail", id=p["id"], _external=True), "lastmod": today})

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append("<url>")
        xml.append(f"<loc>{p['loc']}</loc>")
        xml.append(f"<lastmod>{p['lastmod']}</lastmod>")
        xml.append("</url>")
    xml.append("</urlset>")

    return Response("\n".join(xml), mimetype="application/xml")

if __name__ == "__main__":
    app.run(debug=True)
