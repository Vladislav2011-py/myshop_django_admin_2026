# Імпортуємо необхідні функції Django:
# render — для відображення HTML шаблонів
# get_object_or_404 — отримує об'єкт або повертає 404 помилку
# redirect — для перенаправлення користувача
from django.shortcuts import render, get_object_or_404, redirect

# Імпортуємо моделі з нашого додатку
from .models import Product, Category, Review


# Головна сторінка (каталог товарів)
def index(request):
    # Отримуємо всі товари з бази, сортуємо від нових до старих
    products = Product.objects.all().order_by("-created_at")

    # Передаємо товари в шаблон
    return render(request, "index.html", {
        "products": products
    })


# Сторінка конкретного товару
def product_detail(request, product_id):

    # Отримуємо товар по ID або повертаємо 404
    product = get_object_or_404(Product, id=product_id)

    # Отримуємо всі відгуки для цього товару
    reviews = Review.objects.filter(product=product)

    # Передаємо товар і відгуки в шаблон
    return render(request, "product_detail.html", {
        "product": product,
        "reviews": reviews
    })


# Сторінка всіх категорій
def categories(request):

    # Отримуємо всі категорії
    categories = Category.objects.all()

    # Передаємо їх у шаблон
    return render(request, "categories.html", {
        "categories": categories
    })


# Товари певної категорії
def category_products(request, category_id):

    # Отримуємо категорію або 404
    category = get_object_or_404(Category, id=category_id)

    # Фільтруємо товари по цій категорії
    products = Product.objects.filter(category=category)

    # Відображаємо ті ж index.html, але з фільтром
    return render(request, "index.html", {
        "products": products,
        "category": category
    })


# ➕ Збільшити кількість товару в кошику
def increase_quantity(request, product_id):

    # Отримуємо кошик із сесії (як словник)
    cart = request.session.get("cart", {})

    # Перетворюємо ID в рядок (бо session зберігає ключі як строки)
    product_id = str(product_id)

    # Якщо товар вже є — збільшуємо кількість
    if product_id in cart:
        cart[product_id] += 1
    else:
        # Якщо немає — додаємо з кількістю 1
        cart[product_id] = 1

    # Зберігаємо оновлений кошик у сесії
    request.session["cart"] = cart

    # Повертаємо користувача в кошик
    return redirect("cart")


# ➖ Зменшити кількість товару
def decrease_quantity(request, product_id):

    # Отримуємо кошик
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        # Зменшуємо кількість
        cart[product_id] -= 1

        # Якщо стало 0 або менше — видаляємо товар
        if cart[product_id] <= 0:
            del cart[product_id]

    # Зберігаємо зміни
    request.session["cart"] = cart

    return redirect("cart")


# Відображення кошика
def cart_view(request):

    # Отримуємо кошик із сесії
    cart = request.session.get("cart", {})

    # Отримуємо товари з бази по ID
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []  # список товарів у кошику
    total = 0        # загальна сума

    for product in products:
        # Кількість товару
        quantity = cart[str(product.id)]

        # Сума за цей товар
        item_total = product.price * quantity

        # Додаємо у список
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "total": item_total
        })

        # Додаємо до загальної суми
        total += item_total

    # Передаємо в шаблон
    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })


# ❌ Видалити товар з кошика повністю
def remove_from_cart(request, product_id):

    # Отримуємо кошик
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    # Якщо товар є — видаляємо
    if product_id in cart:
        del cart[product_id]

    # Зберігаємо
    request.session["cart"] = cart

    return redirect("cart")

# def cart_count(request):
#
#     cart = request.session.get("cart", {})
#
#     total_items = sum(cart.values())
#
#     return {
#         "cart_count": total_items
#     }

def add_to_cart(request, product_id):

    #cart = request.session.get("cart", dict())
    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart = request.session['cart']
    print(type(cart))
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart

    return redirect("cart")