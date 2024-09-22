from django.views.generic import TemplateView
from capybuyra.models import Orders 
# Create your views here.

class ShowOrdersView(TemplateView):
    template_name = "orders/show_orders.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['orders'] = Orders.objects.all()

        return context