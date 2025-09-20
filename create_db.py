from app import app, db
from app import Product  # مدل Product از app.py

# فعال کردن context اپلیکیشن
with app.app_context():
    # ساخت جداول دیتابیس
    db.create_all()

    # بررسی اینکه آیا دیتابیس قبلاً پر شده
    if not Product.query.first():
        # تعریف 8 محصول نمونه
        products = [
            Product(
                name="تخت خواب کلاسیک",
                price=2500000,
                image="bed1.jpg",
                rating=4.5,
                short_description="تختی با کیفیت و طراحی کلاسیک",
                description="این تخت خواب کلاسیک با چوب مرغوب و طراحی زیبا مناسب هر اتاق خواب است.",
                tag="جدید"
            ),
            Product(
                name="تخت خواب مدرن",
                price=3000000,
                image="bed2.jpg",
                rating=4.8,
                short_description="تختی مدرن و شیک",
                description="این تخت خواب مدرن با طراحی مینیمال و کیفیت بالا آماده خدمت‌رسانی است.",
                tag="پرفروش"
            ),
            Product(
                name="تخت خواب نوجوان",
                price=1800000,
                image="bed3.jpg",
                rating=4.2,
                short_description="تخت مناسب اتاق نوجوانان",
                description="این تخت با طراحی جذاب و اندازه مناسب برای اتاق نوجوانان ایده‌آل است.",
                tag="جدید"
            ),
            Product(
                name="تخت خواب دونفره راحت",
                price=3500000,
                image="bed4.jpg",
                rating=4.7,
                short_description="تخت دونفره با راحتی بالا",
                description="این تخت دونفره با راحتی بالا و کیفیت ساخت عالی، خواب شما را بهبود می‌بخشد.",
                tag="پرفروش"
            ),
            Product(
                name="تخت خواب یک نفره ساده",
                price=1200000,
                image="bed5.jpg",
                rating=4.0,
                short_description="تخت ساده و اقتصادی",
                description="تخت یک نفره ساده و اقتصادی با دوام مناسب برای استفاده روزمره.",
                tag=""
            ),
            Product(
                name="تخت خواب کم جا",
                price=2000000,
                image="bed6.jpg",
                rating=4.3,
                short_description="تخت کم جا برای فضای کوچک",
                description="این تخت مناسب فضاهای کوچک است و طراحی مدرن و کاربردی دارد.",
                tag="جدید"
            ),
            Product(
                name="تخت خواب لوکس چوبی",
                price=4500000,
                image="bed7.jpg",
                rating=4.9,
                short_description="تخت لوکس از چوب طبیعی",
                description="تخت خواب لوکس ساخته شده از چوب طبیعی با طراحی شیک و دوام بالا.",
                tag="پرفروش"
            ),
            Product(
                name="تخت خواب شیک مینیمال",
                price=2800000,
                image="bed8.jpg",
                rating=4.6,
                short_description="تخت شیک و مینیمال",
                description="این تخت خواب مینیمال با طراحی مدرن و ساده مناسب اتاق‌های کوچک و بزرگ است.",
                tag=""
            )
        ]

        # اضافه کردن محصولات به دیتابیس
        db.session.add_all(products)
        db.session.commit()
        print("دیتابیس ساخته شد و ۸ محصول نمونه اضافه شدند.")
    else:
        print("محصولات اولیه قبلاً اضافه شده‌اند.")
