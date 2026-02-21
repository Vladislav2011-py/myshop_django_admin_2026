from ipaddress import collapse_addresses

from django.contrib import admin
from .models import Product

# Register your models here.
# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'in_stock', 'created_at']
    list_filter = ['in_stock', 'created_at']
    search_fields = ['name', 'description']
    list_per_page = 20
    ordering = ['-created_at']
    date_hierarchy = "created_at"
    readonly_fields = ['created_at']
    fieldsets = (
        ("Основна інформація", {
            "fields": ('name', 'description')
        }),
        ("Ціна та наявність", {
            "fields": ('price', 'in_stock')
        }),
        ("Додаткова інформація", {
            "fields": ('created_at',),
            "classes": ('collapse',)
        }),
    )