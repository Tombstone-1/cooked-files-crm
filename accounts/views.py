from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here./views and models name shouldn't be same.case senstive
from .models import *
from .forms import *
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# using login required and is_authenticate method is bad design .change to middleware

################################# Authenticate ##################################
# there is one more method using usercreation form
@unauthenticated_user
def registerPage(request):
    """
    if request.user.is_authenticated:
        return redirect('home')
    else:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password2 == password1:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'User already exists')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email taken')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                # linking user to a customer
                Customer.objects.create(
                    user=user,
                    name=username,
                    email=email,
                )
                # for adding user to a group
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                
                messages.success(request, 'Account created for user ' + username)
                return redirect("login")
        else:
            messages.error(request, 'check confirmed password again')


    return render(request, "register.html")

@unauthenticated_user
def loginPage(request):
    """
    if request.user.is_authenticated:    # is_authenticated is a property, used to stop view login when logged in.
        return redirect('home')
    else:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, ' incorrect Username or Password')

    return render(request, "login.html")

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def Home(request):
    customer = Customer.objects.all()
    order = Order.objects.all()

    total = order.count()
    delivered = order.filter(status='Delivered').count()
    shipping = order.filter(status='Shipping').count()
    out_way = order.filter(status='On the way').count()
    cancelled = order.filter(status='Cancelled').count()
    recent = order.order_by('-date_update')[:5]  # fetch last orders acc update

    context = {
    'customer':customer,'order':order,
    'total':total, 'delivered':delivered,
    'shipping':shipping, 'out_way':out_way,
    'cancelled':cancelled, 'recent':recent,
    }
    return render(request, 'accounts/dashboard.html', context)

########################### User/customer links ###################################

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    recent = orders.order_by('-date_update')[:5]
    total = orders.count()
    delivered = orders.filter(status='Delivered').count()

    context = {
    'recent':recent,
    'total':total, 'delivered':delivered,
    }
    return render(request, 'accounts/user-dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):
    customer = Customer.objects.get(email=request.user.email)
    orders = customer.order_set.all()
    count = orders.count()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context = {
        'customer':customer, 'orders':orders,
        'count':count, 'filter':order_filter
    }
    return render(request, 'accounts/user-profile.html', context)

################################ Customers ###################################

@login_required(login_url='login')
@admin_only
def Customers(request):
    customer = Customer.objects.all()

    context = {'customers':customer}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@admin_only
def Customers_profile(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    count = orders.count()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context = {
        'customer':customer, 'orders':orders,
        'count':count, 'filter':order_filter
    }
    return render(request, 'accounts/customer_profile.html', context)

@login_required(login_url='login')
@admin_only
def customer_create(request):
    form = customerForm()
    if request.method == 'POST':
        form = customerForm(request.POST, request.FILES) # request.FILES for images
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/customer_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_update(request, pk):
    query = Customer.objects.get(id=pk)
    form = customerForm(instance=query)
    if request.method =='POST':
        form = customerForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/customer_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_delete(request, pk):
    query = Customer.objects.get(id=pk)
    if request.method == 'POST':
        query.delete()
        return redirect('login')

    context = {'customer':query}
    return render(request, 'accounts/customer_delete.html', context)


################################# Products ##################################

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def Products(request):
    product = Product.objects.all()

    context = {'products':product}
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_product(request):
    form = productForm()
    if request.method == 'POST':
        form = productForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')

    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)

@login_required(login_url='login')
@admin_only
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = productForm(instance=product)
    if request.method == 'POST':
        form = productForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)

@login_required(login_url='login')
@admin_only
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/products/')

    context = {'item':product}
    return render(request, 'accounts/product_delete.html', context)


################################# Orders ####################################

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def order_create(request, pk):
    customer = Customer.objects.get(id=pk)

    # args== Parent modelname, Child modelname, field you want to show , and how many order selection form.
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'quantity', 'status'), extra=3)
    formset = orderFormSet(queryset=Order.objects.none(), instance=customer) #for showing no prefill forms but mutiple forms

    #form = orderForm(initial={'customer':customer}) #for approch parent model inside form
    if request.method == 'POST':
        #form = orderForm(request.POST)
        formset = orderFormSet(request.POST, instance=customer) #always put request then instance for prefilling rest you know.
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def order_update(request, pk):
    query = Order.objects.get(id=pk)
    form = orderForm(instance=query)
    if request.method =='POST':
        form = orderForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def order_delete(request, pk):
    query = Order.objects.get(id=pk)
    if request.method == 'POST':
        query.delete()
        return redirect('/')

    context = {'item':query}
    return render(request, 'accounts/order_delete.html', context)
