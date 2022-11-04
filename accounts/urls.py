from django.urls import path
from .import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register'),

    path('user-page', views.userPage, name='user-page'),
    path('user-profile', views.userProfile, name='user-profile'),
    path('user-delete/<str:pk>/', views.userDelete, name='user-delete'),


    path('products/', views.Products, name='products'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<str:pk>/', views.update_product, name='update_product'),
    path('delete_product/<str:pk>/', views.delete_product, name='delete_product'),


    path('customer/', views.Customers, name='customer'),
    path('customers_profile/<str:pk>/', views.Customers_profile, name='customers_profile'),
    path('customer_create/', views.customer_create, name='customer_create'),
    path('customer_update/<str:pk>/', views.customer_update, name='customer_update'),
    

    path('order_create/<str:pk>', views.order_create, name='order_create'), #multiple order(formset) with customer prefilled
    path('order_update/<str:pk>/', views.order_update, name='order_update'),
    path('order_delete/<str:pk>/', views.order_delete, name='order_delete'),
    

]