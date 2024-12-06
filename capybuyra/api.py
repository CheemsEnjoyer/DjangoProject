from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from capybuyra.models import *
from capybuyra.serializers import *
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Max, Min
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
import pyotp
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view

class OrdersViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Orders.objects.all()

    serializer_class = OrdersSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        if status:
            qs = qs.filter(status=status)
        return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg_sum = serializers.FloatField()
        max_sum = serializers.FloatField()
        min_sum = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = self.get_queryset().aggregate(
            count=Count('id'),
            avg_sum=Avg('sum'),
            max_sum=Max('sum'),
            min_sum=Min('sum'),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class CustomerViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return Customer.objects.none()


class CategoryViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if self.request.user.is_superuser:
    #         user_id = self.request.query_params.get('user_id')
    #         if user_id:
    #             qs = qs.filter(user_id=user_id)
    #     else:
    #         qs = qs.filter(user=self.request.user)
    #     return qs

    
class ProductViewSet(mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin, 
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        
        # if self.request.user.is_superuser:
        #     user_id = self.request.query_params.get('user_id')
        #     if user_id:
        #         qs = qs.filter(user_id=user_id)
        # else:
        #     qs = qs.filter(user=self.request.user)
        
        if category_id:
            qs = qs.filter(category_id=category_id)
        
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            qs = qs.filter(cost__gte=min_price)
        if max_price:
            qs = qs.filter(cost__lte=max_price)
            
        return qs


class ShoppingCartViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["GET"], url_path="my_cart")
    def my_cart(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Неавторизованный пользователь"}, status=401)

        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        if not shopping_cart:
            return Response({"items": [], "total": 0})

        serializer = self.get_serializer(shopping_cart)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path="remove/(?P<product_id>[^/.]+)")
    def remove_product(self, request, product_id=None):
        try:
            shopping_cart = ShoppingCart.objects.get(user=request.user)
            item = ProductShoppingCart.objects.get(
                shopping_cart=shopping_cart, product_id=product_id
            )
            item.delete()
            return Response({"message": "Товар удалён из корзины."}, status=status.HTTP_204_NO_CONTENT)
        except ProductShoppingCart.DoesNotExist:
            return Response(
                {"error": "Товар не найден в корзине."}, status=status.HTTP_404_NOT_FOUND
            )
        except ShoppingCart.DoesNotExist:
            return Response(
                {"error": "У пользователя нет корзины."}, status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        qs = super().get_queryset()

        if not(self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)
        return qs
    
class ReviewViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if self.request.user.is_superuser:
    #         user_id = self.request.query_params.get('user_id')
    #         if user_id:
    #             qs = qs.filter(user_id=user_id)
    #     else:
    #         qs = qs.filter(user=self.request.user)
    #     return qs
    
class ProductShoppingCartViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = ProductShoppingCart.objects.all()
    serializer_class = ProductShoppingCartSerializer

    queryset = User.objects.all()
    serializer_class = UserSerializer

    
class OrderProductViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

class UserProfileViewset(GenericViewSet):
    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
        user = self.request.user
        user_info = {
            "is_authenticated": user.is_authenticated
        }
        if user.is_authenticated:
            user_info.update({
                "is_superuser": user.is_superuser,
                "username": user.username
            })
        
        return Response(user_info)

    @action(detail=False, methods=["POST"], url_path="register")
    def register_user(self, request):
        data = request.data
        if not all(key in data for key in ['username', 'first_name', 'last_name', 'email', 'password']):
            return Response({'error': 'Все поля обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Пользователь с таким email уже существует.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=data['username']).exists():
            return Response({'error': 'Пользователь с таким username уже существует.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password']
        )

        return Response({'message': 'Пользователь успешно зарегистрирован!'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login', permission_classes=[])
    def login(self, request, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        
        return Response({
            'is_auth': bool(user)
        })
    
    @action(detail=False, methods=['get'], url_path='logout', permission_classes=[])
    def logout(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            #request.user.auth_token.delete()
            logout(request)
        return Response({
            'is_auth': False
        })
    
    @action(detail=False, methods=["GET"], url_path="initialize")
    def initialize_auth(self, request, *args, **kwargs):
        user = self.request.user
        user_info = {
            "is_authenticated": user.is_authenticated,
            "username": user.username if user.is_authenticated else "",
            "is_superuser": user.is_superuser if user.is_authenticated else False
        }
        return Response(user_info, status=status.HTTP_200_OK)
    
    @action(url_path="all", methods=["GET"], detail=False)
    def list_users(self, request, *args, **kwargs):
        users = User.objects.all().values("id", "username", "is_superuser")
        return Response(list(users))


class AddToCartViewSet(GenericViewSet):
    def create(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            cart, created = ShoppingCart.objects.get_or_create(user=user)

            product = Product.objects.get(id=product_id)

            cart_item, created = ProductShoppingCart.objects.get_or_create(
                shopping_cart=cart,
                product=product,
            )
            if not created:
                cart_item.quantity += int(quantity)
            cart_item.save()

            return Response({'message': 'Товар добавлен в корзину'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)