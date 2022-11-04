from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True, blank=False, unique=True)
	phone = models.CharField(max_length=14, null=True)
	country = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profileM.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Customers'

class Tag(models.Model):
	name = models.CharField(max_length=20, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Tags'

class Product(models.Model):
	CATEGORY = (
		('Appliances', 'Appliances'),
		('Computer & Accessories', 'Computer & Accessories'),
		('Electronics', 'Electronics'),
		('Home & Kitchen', 'Home & Kitchen'),
		('Garden & Outdoors', 'Garden & Outdoors'),
		('Furniture', 'Furniture'),	
		('Fashion Wears', 'Fashion Wears'),
		('Sports & Fitness', 'Sports & Fitness'),
		)

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.TextField( null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Products'

class Order(models.Model):
	STATUS = (
		('Shipping', 'Shipping'),
		('On the way', 'On the way'),
		('Delivered', 'Delivered'),
		('Cancelled', 'Cancelled'),	
		)

	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL) #models.CASCADE #models.PROTECT
	quantity = models.IntegerField(default=1)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	date_update = models.DateTimeField(auto_now = True, blank=True) # adds date everytime
	date_created = models.DateTimeField(auto_now_add=True, blank=True) #adds date initially

	def __str__(self):
		return self.product.name

	class Meta:
		verbose_name_plural = 'Orders'
