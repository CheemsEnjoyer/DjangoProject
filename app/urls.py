"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from capybuyra import views
from rest_framework.routers import DefaultRouter
from capybuyra.api import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('orders', OrdersViewSet, basename='orders')
router.register('customers', CustomerViewSet, basename='customers')
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')
router.register('shoppingcarts', ShoppingCartViewSet, basename='shoppingcarts')
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('user', UserProfileViewset, basename='user')
router.register('add_to_cart', AddToCartViewSet, basename='add_to_cart')

urlpatterns = [
    path('', views.ShowOrdersView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
