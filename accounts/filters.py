import django_filters

from .models import Order

class OrderFilter(django_filters.FilterSet):
	
	class Meta:
		model = Order
		fields = ['product', 'status', 'quantity']
		exclude = ['customer','date_updated','date_created']