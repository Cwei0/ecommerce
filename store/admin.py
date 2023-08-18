"""
Django Admin Configuration for Ecommerce App

This module configures the Django admin interface for managing Category and Product models
in an ecommerce application. It defines customizations for displaying, filtering, and editing
fields in the admin list views, as well as prepopulating the 'slug' field based on another field's value.

Author: Bott Gabriel

Usage:
    This code should be placed in the 'admin.py' file of your Django app to customize the admin interface
    for the Category and Product models.

Example:
    # admin.py

    from django.contrib import admin
    from .models import Category, Product

    # Register your models here.
    @admin.register(Category)
    class CategoryAdmin(admin.ModelAdmin):
        # ... (CategoryAdmin customization)

    @admin.register(Product)
    class ProductAdmin(admin.ModelAdmin):
        # ... (ProductAdmin customization)


"""
from django.contrib import admin
from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "slug",
        "price",
        "in_stock",
        "created",
        "updated",
    ]
    list_filter = ["in_stock", "is_active"]
    list_editable = ["price", "in_stock"]
    prepopulated_fields = {"slug": ("title",)}
