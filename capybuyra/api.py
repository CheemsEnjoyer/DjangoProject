from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from capybuyra.models import *
from capybuyra.serializers import *
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Max, Min
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.cache import cache
import pyotp
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework import status

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
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
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

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs

    
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
        
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        
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

    def get(self, request):
        try:
            cart = ShoppingCart.objects.get(user=request.user)
            serializer = ShoppingCartSerializer(cart)
            return Response(serializer.data)
        except ShoppingCart.DoesNotExist:
            return Response({'error': 'Корзина не найдена'}, status=404)
        
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

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs
    
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

    @action(url_path="all", methods=["GET"], detail=False)
    def list_users(self, request, *args, **kwargs):
        users = User.objects.all().values("id", "username", "is_superuser")
        return Response(list(users))
    
    permission_classes = [IsAuthenticated]

    class OTPSerializer(serializers.Serializer):
        key = serializers.CharField()

    class OTPRequired(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and cache.get('otp_good', False))
        
    @action(detail=False, url_path="check-login", methods=['GET'], permission_classes=[])
    def get_check_login(self, request, *args, **kwargs):
        return Response({
            'is_authenticated': self.request.user.is_authenticated
        })
    
    @action(detail=False, url_path="login", methods=['GET'], permission_classes=[])
    def use_login(self, request, *args, **kwargs):
        user= authenticate(username='username', password='pass')
        if user:
            login(request, user)
        return Response({
            'is_authenticated': bool(user)
        })

    @action(detail=False, url_path='otp-login', methods=['POST'], serializer_class=OTPSerializer)
    def otp_login(self, *args, **kwargs):
        totp = pyotp.TOTP(self.request.user.userprofile.opt_key)
        
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        success = False
        if totp.now() == serializer.validated_data['key']:
            cache.set('otp_good', True, 10)
            success = True

        return Response({
            'success': success
        })
    
    @action(detail=False, url_path='otp-status')
    def get_otp_status(self, *args, **kwargs):
        otp_good = cache.get('otp_good', False)
        return Response({
            'otp_good': otp_good
        })
    
    @action(detail=False, url_path='otp-required', permission_classes=[OTPRequired])
    def page_with_otp_required(self, *args, **kwargs):
        return Response({
            'success': True
        })


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