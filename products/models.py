from django.db import models
from django.db.models import EmailField, CharField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "КатегоріЇ"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null = True,
        blank = True,
        verbose_name="Категорія"
    )
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    in_stock = models.BooleanField(default=True, verbose_name="В наявності")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(null=True, blank=True)

# Замовлення
# Номер замовлення та інформація про покупця
# Створюється підтвердження оплати
class Order (models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_DELIVERED = 'delivered'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Очікує оплати'),
        (STATUS_PAID, 'Оплачено'),
        (STATUS_FAILED, 'Помилка оплати'),
        (STATUS_FAILED, 'Доставлено')
    ]
#     list_products = []

    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер транзакції'
    )

    customer_name = models.CharField(
        max_length=200,
        verbose_name=''
    )

    email_field = models.EmailField(
        max_length=100,
        verbose_name='Email покупця'
    )

    customer_phone = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Email покупця'
    )

    delivery_adress = models.TextField(
            blank=True,
            verbose_name='Адреса доставки'
        )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Загальна сума'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='Статус'
    )

    liqpay_payment_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Id платежу LiqPay'
    )

    liqpay_status = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Статус Liqpay'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата замовлення'
    )

    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Оновлено'
    )

    class Meta:
        verbose_name='Замовлення',
        verbose_name_plural = 'Замовлення',
        ordering = ['-created_at']

    def __str__(self):
        # Замовлення 345 - Аладін
        return f'Замовлення #{self.order_number} - {self.customer_name}'

# Товари в замовлені
# Що і в якій кільскості замовлення

class OrderItem (models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Замовлення'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Товар'
    )

    product_name = models.CharField(
        max_length=200,
        verbose_name='Назва товару'
    )

    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Ціна на момент замовлення'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Кількість'
    )

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'

    @property
    def total_price(self):  # object.total_price()
        """Ціна цієї позиції (ціна * кільсість)"""
        return self.product.price * self.quantity  # 75 * 2  --> 150

# Зберігається інформація у браузері
class CartItem(models.Model):
    # session_key - ключ сесії браузера
    session_key = models.CharField(
        max_length=50,
        verbose_name='Ключ сессії'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name = Product
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Кількість'
    )

    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Додано'
    )

    class Meta:
        verbose_name = 'Елемент кошика',
        verbose_name_plural = 'Кошик',
        unique_together = ['session_key', 'product']

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'  #томат х2

    @property
    def total_price(self):  # object.total_price()
        """Ціна цієї позиції (ціна * кільсість)"""
        return self.product.price * self.quantity  # 75 * 2  --> 150

