# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# ---------- تنظیمات اصلی Flask ----------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # تغییر بده به یک کلید امن
db = SQLAlchemy(app)

# ---------- مدل محصول ----------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    excerpt = db.Column(db.String(200))
    image = db.Column(db.String(200))

# ---------- پنل مدیریتی ----------
admin = Admin(app, name='پنل مدیریت', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))

# ---------- مسیر صفحه اصلی ----------
@app.route('/')
def home():
    products = Product.query.all()  # خواندن تمام محصولات از دیتابیس
    meta = {'site_name': 'کارخانه تخت خواب ایرانیان'}
    return render_template('index.html', products=products, meta=meta)

# ---------- اجرای برنامه ----------
if __name__ == '__main__':
    db.create_all()  # ایجاد دیتابیس SQLite و جدول‌ها
    app.run(debug=True)
