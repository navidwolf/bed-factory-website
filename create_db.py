from app import app, db, Admin
from werkzeug.security import generate_password_hash
import os

# مطمئن شدن از وجود پوشه instance
if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance")):
    os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance"))

with app.app_context():
    db.create_all()
    
    # ایجاد ادمین پیشفرض
    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin", password=generate_password_hash("admin123"))
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin already exists")
