from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from capybuyra.models import Orders 
# Create your views here.

def ShowOrdersView(View):
    def get(request, *args, **kwargs):
        orders = Orders.objects.all()

        result = ''
        for o in orders:
            result += s.name + "<br>"

        return HttpResponse(result)