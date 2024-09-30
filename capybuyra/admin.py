from django.contrib import admin

# Register your models here.
from capybuyra.models import Orders, Client, Product, Category, ShoppingCart, ProductShoppingCart, OrderProduct, Review

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', "client_id", "sum", "status"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [ 'id','name', 'password', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cost', 'description', 'amount', 'category_id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'sum', 'client_id']


@admin.register(ProductShoppingCart)
class ProductShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'shoppingCart_id']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'order_id']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'rating', 'client_id', 'product_id']