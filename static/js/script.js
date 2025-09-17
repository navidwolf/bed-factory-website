document.addEventListener("DOMContentLoaded", function() {

    // افزودن محصول به سبد خرید از صفحه محصولات
    document.querySelectorAll(".add-to-cart-btn-ajax").forEach(btn => {
        btn.addEventListener("click", function() {
            const product_id = this.dataset.id;
            fetch("/add_to_cart_ajax/" + product_id, { method: "POST" })
            .then(response => response.json())
            .then(data => {
                const cartCountElem = document.getElementById("cart-count");
                if(cartCountElem) cartCountElem.textContent = data.total_items;
                alert("محصول به سبد خرید اضافه شد!");
            });
        });
    });

    // بروزرسانی سبد خرید در cart.html
    function updateCart(product_id, action) {
        fetch("/update_cart_ajax", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: product_id, action: action })
        })
        .then(response => response.json())
        .then(data => {
            for (const [id, item] of Object.entries(data.cart)) {
                const row = document.querySelector(`tr[data-id='${id}']`);
                if (row) {
                    row.querySelector(".quantity").textContent = item.quantity;
                    row.querySelector(".price").textContent = item.price * item.quantity;
                }
            }
            document.querySelectorAll("#cart-table tr[data-id]").forEach(row => {
                if (!data.cart[row.dataset.id]) row.remove();
            });
            const totalElem = document.getElementById("total");
            if(totalElem) totalElem.textContent = "جمع کل: " + data.total + " تومان";
        });
    }

    // دکمه‌های افزایش/کاهش و حذف در cart.html
    document.querySelectorAll(".update-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            updateCart(this.dataset.id, this.dataset.action);
        });
    });

    document.querySelectorAll(".remove-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            updateCart(this.dataset.id, "remove");
        });
    });

});
