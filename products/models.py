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

class Order (models.Model):
    list_products = []

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