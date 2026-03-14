from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Review


def index(request):
    products = Product.objects.all().order_by("-created_at")

    return render(request, "index.html", {
        "products": products
    })


def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    reviews = Review.objects.filter(product=product)

    return render(request, "product_detail.html", {
        "product": product,
        "reviews": reviews
    })


def categories(request):

    categories = Category.objects.all()

    return render(request, "categories.html", {
        "categories": categories
    })


def category_products(request, category_id):

    category = get_object_or_404(Category, id=category_id)

    products = Product.objects.filter(category=category)

    return render(request, "index.html", {
        "products": products,
        "category": category
    })


def add_to_cart(request, product_id):

    cart = request.session.get("cart", [])

    if product_id not in cart:
        cart.append(product_id)

    request.session["cart"] = cart

    return redirect("cart")


def cart_view(request):

    cart = request.session.get("cart", [])

    products = Product.objects.filter(id__in=cart)

    total = sum(product.price for product in products)

    return render(request, "cart.html", {
        "products": products,
        "total": total
    })