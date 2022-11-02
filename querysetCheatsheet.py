# provided by Dennis ivy

Product,Order,Customer = 'models name'

# Returns all customer from customer table
customers = Customer.objects.all()

#Returns first customer from customers table
first_customer = Customer.objects.first()

# Returns last customer from customer table
last_customer = Customer.objects.last()

# Returns single customer by name
customerByname = Customer.objects.get(name='Peter')

# Returns single unique customer by id
customerbyId = Customer.objects.get(id=2)

# Returns all orders related to customer (first_customer varibale above, order varible below)
first_customer.order_set.all()

# returns orders customer name (query parent model name)
order = Order.objects.first()
parentName = Order.customer.name

# Returns products from products table with value of 'Out door' in category attribute
products = Product.objects.filter(category='out door')

# Order/Sort objects by id
Accending = Product.objects.all().order_by('id')
Decending = Product.objects.all().order_by('-id')

# Returns all products with tag of 'sports': (Query many to many fields)
# two underscore because we are fetch many to many relation and fetching from products
productFiltered = Product.objects.filter(tags__name='sports')

'''
Bonus
 if 1 customer place more than 1 order how to find that ? (access child class from parent/ forward method )
'''
customer1 = Customer.objects.get(id=2)
orders = customer1.order_set.all()   # even if order model is written in capital you have to write here in all small.
print(orders)

'''
or who placed the first order ?(reverse method / access parent model through child model)
'''
order = Order.objects.first()
print(order.customer.name)

'''
questions if customer has more than one ball, how would you reflect it in the database?

A. Because there are many different products adn this value changes constantly you would most
likely not want to store the value in the database but rather just make this a function we can run
each time we load the customer profile
'''
# returns total the total count for number of time a "ball" was ordered by the first customer
ballorders = first_customer.order_set.filter(product__name='ball').count()

# returns total count for each product ordered ( either put this in model method or views file)
allorders = {}

for order in first_customer.order_set.all():
    if order.product.name in allorders:
        allorders[order.product.name] += 1
    else:
        allorders[order.product.name] = 1

#output Returns: allorders: {'ball' : 2, 'BBQ grill' : 1}

# access child model through parent
class ParentModel(model.Model):
    name = models.CharField(max_length=200)

class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel)
    name = models.CharField(max_length=200)

#first call parent model and store all it value inside a variable
parent = ParentModel.objects.all()
# now returns all value related to parent models from child models
parent.childmodel_set.all()

#variable name.childmodelname_set.all()  in all small