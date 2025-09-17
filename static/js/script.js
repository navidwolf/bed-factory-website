document.addEventListener("DOMContentLoaded", function () {
    // افزودن محصول به سبد خرید
    document.querySelectorAll(".add-to-cart-btn-ajax").forEach(btn => {
        btn.addEventListener("click", function(e){
            e.preventDefault();
            let productId = this.dataset.id;
            fetch("/add_to_cart", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: `id=${productId}&quantity=1`
            })
            .then(res => res.json())
            .then(data => {
                if(data.success){
                    window.location.href = "/cart"; // هدایت به صفحه سبد خرید
                }
            });
        });
    });

    // حذف محصول از سبد خرید
    document.querySelectorAll(".remove-btn").forEach(btn => {
        btn.addEventListener("click", function(){
            let productId = this.dataset.id;
            fetch("/remove_from_cart", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: `id=${productId}`
            })
            .then(res => res.json())
            .then(data => {
                if(data.success){
                    location.reload();
                }
            });
        });
    });

    // افزایش یا کاهش تعداد محصول
    document.querySelectorAll(".update-btn").forEach(btn => {
        btn.addEventListener("click", function(){
            let productId = this.dataset.id;
            let action = this.dataset.action;
            fetch("/update_cart", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: `id=${productId}&action=${action}`
            })
            .then(res => res.json())
            .then(data => {
                if(data.success){
                    location.reload();
                }
            });
        });
    });
});
