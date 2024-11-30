from django.views.generic import TemplateView
from capybuyra.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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

@api_view(['POST'])
def register_user(request):
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