from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "supersecretkey"  # برای session (سبد خرید)

# ================== اطلاعات سایت ==================
meta = {
    "site_name": "کارخانه تخت خواب ایرانیان",
    "address": "تهران، خیابان مثال، پلاک ۱۲۳",
    "phone": "021-12345678",
    "email": "info@example.com"
}

# ================== محصولات ==================
products = [
    {
        "id": 1,
        "title": "تخت خواب مدل کلاسیک",
        "excerpt": "تخت خواب چوبی کلاسیک با طراحی ساده",
        "desc": "این تخت خواب مناسب دکوراسیون سنتی است.",
        "full_desc": "تخت خواب کلاسیک ساخته‌شده از چوب مرغوب...",
        "image": "/static/images/product1.webp"
    },
    {
        "id": 2,
        "title": "تخت خواب مدرن",
        "excerpt": "طراحی مدرن با رنگ‌بندی متنوع",
        "desc": "تخت خواب مناسب اتاق‌های مدرن و امروزی",
        "full_desc": "این تخت خواب با طراحی مدرن و مینیمال...",
        "image": "/static/images/product2.webp"
    },
    {
        "id": 3,
        "title": "تخت خواب سلطنتی",
        "excerpt": "لوکس و شیک برای خانه‌های خاص",
        "desc": "مناسب برای اتاق خواب‌های بزرگ",
        "full_desc": "تخت خواب سلطنتی با تاج‌کاری زیبا...",
        "image": "/static/images/product3.webp"
    },
    {
        "id": 4,
        "title": "تخت خواب نوجوان",
        "excerpt": "مناسب برای نوجوانان با طراحی شاد",
        "desc": "تخت خواب سبک و مقاوم",
        "full_desc": "این تخت خواب با رنگ‌های متنوع برای نوجوانان...",
        "image": "/static/images/product4.webp"
    },
    {
        "id": 5,
        "title": "تخت خواب دو نفره",
        "excerpt": "ساده و شیک برای زوج‌ها",
        "desc": "تخت خواب با ابعاد استاندارد دو نفره",
        "full_desc": "این تخت خواب مقاوم و زیبا...",
        "image": "/static/images/product5.webp"
    },
    {
        "id": 6,
        "title": "تخت خواب تاشو",
        "excerpt": "صرفه‌جویی در فضا برای خانه‌های کوچک",
        "desc": "تاشو و سبک با طراحی کاربردی",
        "full_desc": "این تخت خواب قابلیت جمع شدن دارد...",
        "image": "/static/images/product6.webp"
    },
    {
        "id": 7,
        "title": "تخت خواب طبی",
        "excerpt": "مناسب برای سلامتی و راحتی خواب",
        "desc": "دارای تشک طبی و اسکلت محکم",
        "full_desc": "این تخت خواب برای افرادی که به سلامتی اهمیت می‌دهند...",
        "image": "/static/images/product7.webp"
    },
    {
        "id": 8,
        "title": "تخت خواب مینیمال",
        "excerpt": "طراحی ساده و شیک",
        "desc": "مناسب برای دکوراسیون مدرن",
        "full_desc": "این تخت خواب برای فضاهای کوچک و مینیمالیستی...",
        "image": "/static/images/product8.webp"
    }
]

# ================== مسیرها (Routes) ==================

@app.route("/")
def index():
    return render_template("index.html", meta=meta)

@app.route("/products")
def products_page():
    return render_template("products.html", products=products, meta=meta)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template("product_detail.html", product=product, meta=meta)
    return "محصول پیدا نشد", 404

@app.route("/contact")
def contact():
    return render_template("contact.html", meta=meta)

# ================== اجرای برنامه ==================
if __name__ == "__main__":
    app.run(debug=True)
