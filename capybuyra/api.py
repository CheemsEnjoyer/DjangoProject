from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from capybuyra.models import Orders
from capybuyra.serializers import OrdersSerializer

class OrdersViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer