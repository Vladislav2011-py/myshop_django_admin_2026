from ipaddress import collapse_addresses

from django.contrib import admin
from .models import Product, Category

# Register your models here.
# admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'created_at', 'colored_status']
    list_filter = ['category', 'in_stock', 'created_at']
    autocomplete_fields = ['category']
    search_fields = ['name', 'description']
    list_per_page = 20
    ordering = ['-created_at']
    date_hierarchy = "created_at"
    list_editable = ['price', 'in_stock']
    readonly_fields = ['created_at', 'colored_status']
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

    def colored_status(self, obj):
        if obj.in_stock:
            return "✅ В наявності"
        return "❌ Немає в наявності"
    colored_status.short_description = "Статус"

    actions = ['make_in_stock', 'make_out_of_stock']

    def make_in_stock(self, request, queryset):
        queryset.update(in_stock=True)
        self.message_user(request, "Товари позначено як 'В наявності'")
    make_in_stock.short_description = "Позначити як 'В наявності'"

    def make_out_of_stock(self, request, queryset):
        queryset.update(in_stock=False)
        self.message_user(request, "Товари позначено як 'Немає в наявності'")
    make_out_of_stock.short_description = "Позначити як 'Немає в наявності'"
