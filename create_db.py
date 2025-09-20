from app import db, Product, app

with app.app_context():
    db.create_all()
    
    # نمونه محصولات اولیه
    products = [
        Product(name="تخت محصول 1", price=1200000, image="product1.webp", rating=4.5, short_description="تخت راحت و مدرن", description="توضیحات کامل محصول 1", tag="جدید"),
        Product(name="تخت محصول 2", price=1500000, image="product2.webp", rating=4.8, short_description="تخت با کیفیت عالی", description="توضیحات کامل محصول 2", tag="پرفروش"),
        Product(name="تخت محصول 3", price=1300000, image="product3.webp", rating=4.2, short_description="تخت با طراحی مینیمال", description="توضیحات کامل محصول 3"),
        Product(name="تخت محصول 4", price=1700000, image="product4.webp", rating=5.0, short_description="تخت لوکس و شیک", description="توضیحات کامل محصول 4", tag="جدید"),
        Product(name="تخت محصول 5", price=1250000, image="product5.webp", rating=4.0, short_description="تخت راحت و ارزان", description="توضیحات کامل محصول 5"),
        Product(name="تخت محصول 6", price=1800000, image="product6.webp", rating=4.9, short_description="تخت مدرن و مقاوم", description="توضیحات کامل محصول 6"),
        Product(name="تخت محصول 7", price=1400000, image="product7.webp", rating=4.3, short_description="تخت با طراحی کلاسیک", description="توضیحات کامل محصول 7", tag="پرفروش"),
        Product(name="تخت محصول 8", price=1600000, image="product8.webp", rating=4.7, short_description="تخت شیک و زیبا", description="توضیحات کامل محصول 8")
    ]

    db.session.bulk_save_objects(products)
    db.session.commit()
    print("Database created and products added.")
