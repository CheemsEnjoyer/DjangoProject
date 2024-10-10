from django.contrib import admin

# Register your models here.
from capybuyra.models import *

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'user_id', 'sum', 'status']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cost', 'description', 'amount', 'category_id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'sum', 'user_id']

@admin.register(ProductShoppingCart)
class ProductShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'shopping_cart_id']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'order_id']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'rating', 'user_id', 'product_id']