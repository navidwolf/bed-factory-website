from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)

# ---------------- تنظیمات دیتابیس ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- مدل محصولات ----------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    excerpt = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)

# ---------------- ساخت دیتابیس در هر بار اجرا ----------------
with app.app_context():
    db.create_all()
    if not Product.query.first():
        sample_products = [
            Product(title="تخت خواب مدرن", excerpt="یک مدل نمونه برای تست", image="/static/images/product1.webp"),
            Product(title="سرویس خواب کلاسیک", excerpt="یک مدل دیگر برای تست", image="/static/images/product2.webp"),
        ]
        db.session.add_all(sample_products)
        db.session.commit()

# ---------------- پنل مدیریتی ----------------
admin = Admin(app, name='پنل مدیریت', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))

# ---------------- صفحه اصلی ----------------
@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)

# ---------------- اجرای برنامه ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
