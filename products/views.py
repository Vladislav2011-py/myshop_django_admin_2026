# Імпортуємо необхідні функції Django:
# render — для відображення HTML шаблонів
# get_object_or_404 — отримує об'єкт або повертає 404 помилку
# redirect — для перенаправлення користувача
from django.shortcuts import render, get_object_or_404, redirect

# Імпортуємо моделі з поточної папки (models.py)
from .models import Product, Category, Review

# Головна сторінка (каталог товарів)
def index(request):
    # Отримуємо всі товари з бази, сортуємо від нових до старих
    products = Product.objects.all().order_by("-created_at")

    # Відображаємо шаблон і передаємо товари
    return render(request, "index.html", {
        "products": products
    })


# Детальна сторінка товару
def product_detail(request, product_id):

    # Отримуємо товар по ID або повертаємо 404, якщо не знайдено
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

    # Отримуємо всі категорії з бази
    categories = Category.objects.all()

    # Передаємо їх у шаблон
    return render(request, "categories.html", {
        "categories": categories
    })


# Сторінка товарів конкретної категорії
def category_products(request, category_id):

    # Отримуємо категорію або 404
    category = get_object_or_404(Category, id=category_id)

    # Фільтруємо товари по цій категорії
    products = Product.objects.filter(category=category)

    # Використовуємо той самий шаблон index.html, але з фільтром
    return render(request, "index.html", {
        "products": products,
        "category": category
    })


# ➕ Збільшення кількості товару в кошику
def increase_quantity(request, product_id):

    # Отримуємо кошик із session (якщо немає — створюємо пустий словник)
    cart = request.session.get("cart", {})

    # Перетворюємо product_id у рядок (бо ключі в session — рядки)
    product_id = str(product_id)

    # Якщо товар вже є в кошику — збільшуємо кількість
    if product_id in cart:
        cart[product_id] += 1
    else:
        # Якщо товару ще нема — додаємо з кількістю 1
        cart[product_id] = 1

    # Зберігаємо оновлений кошик у session
    request.session["cart"] = cart

    # Переходимо назад у кошик
    return redirect("cart")


# ➖ Зменшення кількості товару
def decrease_quantity(request, product_id):

    # Отримуємо кошик
    cart = request.session.get("cart", {})

    # Перетворюємо ID у рядок
    product_id = str(product_id)

    # Якщо товар є в кошику
    if product_id in cart:

        # Зменшуємо кількість
        cart[product_id] -= 1

        # Якщо кількість стала 0 або менше — видаляємо товар
        if cart[product_id] <= 0:
            del cart[product_id]

    # Зберігаємо зміни
    request.session["cart"] = cart

    # Повертаємося на сторінку кошика
    return redirect("cart")


# 🛒 Сторінка кошика
def cart_view(request):

    # Отримуємо кошик (формат: {id: quantity})
    cart = request.session.get("cart", {})

    # Отримуємо товари з бази по їх ID
    products = Product.objects.filter(id__in=cart.keys())

    # Список для зручної передачі в шаблон
    cart_items = []

    # Загальна сума
    total = 0

    # Проходимося по кожному товару
    for product in products:

        # Отримуємо кількість товару з кошика
        quantity = cart[str(product.id)]

        # Рахуємо суму для цього товару
        item_total = product.price * quantity

        # Додаємо дані у список
        cart_items.append({
            "product": product,   # сам товар
            "quantity": quantity, # кількість
            "total": item_total   # сума за цей товар
        })

        # Додаємо до загальної суми
        total += item_total

    # Відправляємо дані в шаблон
    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })

# Видалення товару з кошика
def remove_from_cart(request, product_id):

    # Отримуємо кошик
    cart = request.session.get("cart", [])

    # Якщо товар є в кошику — видаляємо
    if product_id in cart:
        cart.remove(product_id)

    # Зберігаємо оновлений кошик
    request.session["cart"] = cart

    # Перенаправляємо назад у кошик
    return redirect("cart")

def add_to_cart(request, product_id):
    pass