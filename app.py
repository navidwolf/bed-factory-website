from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

# تنظیمات دیتابیس SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# مدل محصول
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    excerpt = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)


# ایجاد دیتابیس (فقط بار اول)
with app.app_context():
    db.create_all()


# پنل ادمین
admin = Admin(app, name="پنل مدیریت", template_mode="bootstrap3")
admin.add_view(ModelView(Product, db.session))


# متای سئو برای همه قالب‌ها
@app.context_processor
def inject_meta():
    return {
        "meta": {
            "site_name": "Bed Factory",
            "description": "معرفی کارخانه تخت خواب ایرانیان و محصولات ما",
            "keywords": "تخت خواب، سرویس خواب، مبلمان، کارخانه ایرانیان"
        }
    }


# صفحه اصلی
@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)
