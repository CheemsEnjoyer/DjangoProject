from django.contrib import admin

# Register your models here.
from capybuyra.models import Orders, Client

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', "client_id"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [ 'id','name']