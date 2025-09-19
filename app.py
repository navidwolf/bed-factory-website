{% extends "base.html" %}
{% block content %}
<div class="container mt-4">
    <h1>پنل مدیریت</h1>
    <a href="{{ url_for('admin_logout') }}" class="btn btn-danger mb-3">خروج</a>

    <h2>محصولات</h2>
    <form action="{{ url_for('admin_add_product') }}" method="POST" class="mb-3">
        <input type="text" name="name" placeholder="نام محصول" required>
        <input type="number" name="price" placeholder="قیمت" required>
        <button type="submit" class="btn btn-success">افزودن</button>
    </form>
    <ul class="list-group mb-4">
        {% for product in products %}
            <li class="list-group-item">{{ product.name }} - {{ product.price }} تومان
                <a href="{{ url_for('admin_delete_product', product_id=product.id) }}" class="btn btn-sm btn-danger float-right">حذف</a>
            </li>
        {% endfor %}
    </ul>

    <h2>پیام‌ها</h2>
    <ul class="list-group">
        {% for msg in messages %}
            <li class="list-group-item">{{ msg.name }} ({{ msg.email }}): {{ msg.message }}</li>
        {% endfor %}
    </ul>
</div>
{% endblock %}
