"""
URL configuration for Ecommerce project.

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
from django.urls import path

from Ecommerce_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='homes'),
    path('about/',views.about,name='abouts'),
    # path('products/',views.products,name='product'),
    path('product_list/<str:category>/', views.product_list, name='product_list'),  # This maps the URL to the view
    path('contact/',views.contact,name='contacts'),
    path('cart/',views.cart,name='carts'),
    # URL for adding a product to the cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # URL for removing one quantity of a product from the cart
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # URL for removing all quantities of a specific product from the cart
    path('remove-all-from-cart/<int:product_id>/', views.remove_all_from_cart, name='remove_all_from_cart'),
    # URL for clearing the entire cart
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('Billing-Clear-Cart/',views.Billing_Clear_Cart, name='billing_clear_cart'),
    path('login/',views.login_view,name='login'),
    path('sign-up/',views.sign_up,name='sign_up'),
    path('logout/',views.logout_view,name='logout'),
    path('check-out/',views.check_out,name='checkout'),
    path('billing/',views.billing,name='billing_receipt'),
    path('payment/',views.payments_view,name='payment'),
    path('search/', views.search_results, name='search_results')
]
