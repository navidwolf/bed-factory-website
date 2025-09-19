from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# ------------------
# MODELS
# ------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100))

# ------------------
# ROUTES
# ------------------

@app.route('/')
def index():
    products = Product.query.limit(8).all()  # حالا ۸ محصول می‌گیریم
    html = "<h1>Products:</h1>"
    for p in products:
        html += f"<div><h3>{p.name}</h3><p>{p.description}</p><p>Price: {p.price}</p></div>"
    return render_template_string(html)

# ------------------
# AUTO INIT DATABASE
# ------------------

@app.before_first_request
def init_db():
    db.create_all()
    if not Product.query.first():
        sample_products = [
            {"name": "Bed A", "description": "Comfortable bed A", "price": 299.99, "image": "bed_a.png"},
            {"name": "Bed B", "description": "Comfortable bed B", "price": 349.99, "image": "bed_b.png"},
            {"name": "Bed C", "description": "Comfortable bed C", "price": 399.99, "image": "bed_c.png"},
            {"name": "Bed D", "description": "Comfortable bed D", "price": 279.99, "image": "bed_d.png"},
            {"name": "Bed E", "description": "Comfortable bed E", "price": 319.99, "image": "bed_e.png"},
            {"name": "Bed F", "description": "Comfortable bed F", "price": 359.99, "image": "bed_f.png"},
            {"name": "Bed G", "description": "Comfortable bed G", "price": 389.99, "image": "bed_g.png"},
            {"name": "Bed H", "description": "Comfortable bed H", "price": 329.99, "image": "bed_h.png"},
        ]
        for prod in sample_products:
            db.session.add(Product(**prod))
        db.session.commit()
    print("✅ Database initialized with 8 sample products!")

# ------------------
# RUN
# ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
