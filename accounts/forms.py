from django.forms import ModelForm
from .models import *

# create your forms here.

class orderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'


class customerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'

class productForm(ModelForm):
	class Meta:
		model = Product 
		fields = '__all__'
		exclude = ['description']