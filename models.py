from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    excerpt = db.Column(db.String(250))
    full_desc = db.Column(db.Text)
    image = db.Column(db.String(250))

class SiteMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(150))
    description = db.Column(db.Text)
    phone = db.Column(db.String(50))
    address = db.Column(db.String(250))
    email = db.Column(db.String(100))
