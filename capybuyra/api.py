from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from capybuyra.models import Orders, Client
from capybuyra.serializers import OrdersSerializer, ClientSerializer

class OrdersViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class ClientViewSet(mixins.ListModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin, 
                    GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer