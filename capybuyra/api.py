from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from capybuyra.models import *
from capybuyra.serializers import *

class OrdersViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Orders.objects.all()

    serializer_class = OrdersSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CustomerViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class CategoryViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class ProductViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ShoppingCartViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class ReviewViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class ProductShoppingCartViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = ProductShoppingCart.objects.all()
    serializer_class = ProductShoppingCartSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class OrderProductViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class UserViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,  
                    GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)