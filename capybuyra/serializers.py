from rest_framework import serializers
from capybuyra.models import *
from django.contrib.auth.models import User

from rest_framework import serializers
from capybuyra.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    user  = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)

    class Meta:
        model = Customer
        fields = "__all__"

class OrdersSerializer(serializers.ModelSerializer):
    user  = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False)

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data["user"] = self.context['request'].user
        return super().create(validated_data)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs


    class Meta:
        model = Orders
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False)

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data["user"] = self.context['request'].user
        return super().create(validated_data)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    user  = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False)

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data["user"] = self.context['request'].user
        return super().create(validated_data)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs
    
    class Meta:
        model = Product
        fields = "__all__"

class ShoppingCartSerializer(serializers.ModelSerializer):
    user  = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False)

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data["user"] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = ShoppingCart
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    user  = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data["user"] = self.context['request'].user
        return super().create(validated_data)
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs
    class Meta:
        model = Review
        fields = "__all__"

class ProductShoppingCartSerializer(serializers.ModelSerializer):
    shoppingCart = ShoppingCartSerializer(read_only=True)
    shoppingCart_id = serializers.PrimaryKeyRelatedField(queryset=ShoppingCart.objects.all(), source='shoppingCart', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    product_cost = serializers.DecimalField(source='product.cost', max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = ProductShoppingCart
        fields = "__all__"

class OrderProductSerializer(serializers.ModelSerializer):
    order = OrdersSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all(), source='order', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    class Meta:
        model = OrderProduct
        fields = "__all__"
