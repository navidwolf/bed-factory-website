from app import db, Product, app

# ایجاد دیتابیس با application context
with app.app_context():
    db.create_all()

    # نمونه محصولات اولیه
    initial_products = [
        Product(name="تخت محصول 1", price=1200000, rating=4.5, image="product1.webp", tag="جدید"),
        	Product(name="تخت محصول 2", price=1350000, rating=4.2, image="product2.webp"),
        Product(name="تخت محصول 3", price=1100000, rating=4.0, image="product3.webp"),
        Product(name="تخت محصول 4", price=1250000, rating=4.7, image="product4.webp"),
        Product(name="تخت محصول 5", price=1400000, rating=4.8, image="product5.webp", tag="پرفروش"),
        	Product(name="تخت محصول 6", price=1500000, rating=4.9, image="product6.webp"),
        Product(name="تخت محصول 7", price=1300000, rating=4.6, image="product7.webp"),
        Product(name="تخت محصول 8", price=1450000, rating=4.4, image="product8.webp"),
    ]

    # افزودن به دیتابیس
    for prod in initial_products:
        db.session.add(prod)
    db.session.commit()

    print("Database created and initial products added successfully.")