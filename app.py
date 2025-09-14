from flask import Flask, render_template
from flask_admin import Admin
from datetime import datetime

# ایجاد اپلیکیشن
app = Flask(__name__)

# تنظیمات Flask-Admin
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

# نمونه داده‌ها
products = [
    {"name": "Bed Model A", "price": 250},
    {"name": "Bed Model B", "price": 300},
]

meta = {
    "site_name": "Bed Factory"
}

# Route اصلی
@app.route('/')
def index():
    current_year = datetime.now().year  # سال جاری
    return render_template('index.html', meta=meta, products=products, current_year=current_year)

# اگر بخواهیم مستقیم با Python اجرا شود
if __name__ == '__main__':
    app.run(debug=True)
