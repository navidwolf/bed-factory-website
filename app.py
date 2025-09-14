from flask import Flask, render_template
from flask_admin import Admin
from datetime import datetime

app = Flask(__name__)
admin = Admin(app, name="Admin", template_mode="bootstrap3")

# Example meta and products
meta = {"site_name": "Bed Factory"}
products = [
    {"name": "Bed A", "price": 100},
    {"name": "Bed B", "price": 150},
]

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.route("/")
def index():
    return render_template("index.html", meta=meta, products=products)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
