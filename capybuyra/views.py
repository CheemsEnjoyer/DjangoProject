from django.views.generic import TemplateView
from capybuyra.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.

class ShowOrdersView(TemplateView):
    template_name = "orders/show_orders.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['orders'] = Orders.objects.all()

        return context

class ShowClientsView(TemplateView):
    template_name = "orders/show_orders.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.all()

        return context