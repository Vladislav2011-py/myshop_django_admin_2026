"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
Тут описуються всі маршрути (URL), які ведуть до певних сторінок (views).
"""

# Адмін-панель Django
from django.contrib import admin

# Функція path для створення URL-маршрутів
from django.urls import path

# Для роботи з медіа файлами (зображення, файли)
from django.conf.urls.static import static
from django.conf import settings

# Імпортуємо всі view-функції з додатку products
from products import views


# Основний список маршрутів сайту
urlpatterns = [

    # Адмінка Django (/admin/)
    path('admin/', admin.site.urls),

    # Головна сторінка (каталог товарів)
    path('', views.index, name='home'),

    # Сторінка конкретного товару (по ID)
    # Наприклад: /product/1/
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Список усіх категорій
    # /categories/
    path('categories/', views.categories, name='categories'),

    # Товари певної категорії
    # /category/2/
    path('category/<int:category_id>/', views.category_products, name='category_products'),

    # Сторінка кошика
    # /cart/
    path('cart/', views.cart_view, name='cart'),

    # ➕ Збільшити кількість товару в кошику
    # /increase/1/
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),

    # ➖ Зменшити кількість товару
    # /decrease/1/
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),

    # ❌ Повністю видалити товар з кошика
    # /remove-from-cart/1/
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]


# Додаємо обробку медіа-файлів (зображень) у режимі розробки
# MEDIA_URL — URL доступу до файлів
# MEDIA_ROOT — папка, де вони зберігаються
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)