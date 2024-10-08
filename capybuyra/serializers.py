from rest_framework import serializers
from capybuyra.models import *
from django.contrib.auth.models import User

from rest_framework import serializers
from capybuyra.models import *
from django.contrib.auth.models import User

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class OrdersSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)  # Переименовано client_id на customer_id
    class Meta:
        model = Orders
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    class Meta:
        model = Product
        fields = "__all__"

class ShoppingCartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)  # Переименовано client_id на customer_id
    class Meta:
        model = ShoppingCart
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)  # Переименовано client_id на customer_id
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)  # Исправлено: запрос должен быть к Product
    class Meta:
        model = Review
        fields = "__all__"

class ProductShoppingCartSerializer(serializers.ModelSerializer):
    shoppingCart = ShoppingCartSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='shoppingCart', write_only=True)  # Переименовано client_id на customer_id
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)  # Исправлено: запрос должен быть к Product
    class Meta:
        model = ProductShoppingCart
        fields = "__all__"

class OrderProductSerializer(serializers.ModelSerializer):
    order = OrdersSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all(), source='order', write_only=True)  # Исправлено: запрос должен быть к Orders
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)  # Исправлено: запрос должен быть к Product
    class Meta:
        model = OrderProduct
        fields = "__all__"
