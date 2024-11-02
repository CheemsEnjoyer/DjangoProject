from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from capybuyra.models import *
from capybuyra.serializers import *
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission

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
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
        return qs

class ShoppingCartViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

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

        if not(self.request.user.is_superuser):
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

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class UserViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]