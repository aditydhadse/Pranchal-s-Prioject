from django.shortcuts import render
from .models import Products, Cart, ContactForm


# Related to cart functionalities
from django.shortcuts import render, redirect, get_object_or_404  # Import necessary Django functions
from .models import Products, Cart  # Import models for Products and Cart
from django.contrib.auth.decorators import login_required  # Decorator to ensure views are accessed only by logged-in users

# Related to login functionalities
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

# Below to make sure users get redirected to source page
from django.http import HttpResponseRedirect
from urllib.parse import urlparse

# AJAX Below for page not being reloaded everytime you add or remove
from django.http import JsonResponse

# Below for Generating Random Order ID
import random

# Below for Date
import datetime as dt

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q  # For Search Results -> Feature in django orm that allows you to build complex database query condition

# Create your views here.
def home(request):
    return render(request,'Home.html')

def about(request):
    return render(request,'About Us.html')

def phones(request):
    return render(request,'Phones.html')

def contact(request):
    if request.method=='POST':
        username=request.POST['uname']
        useremail=request.POST['umail']
        usersub=request.POST['usub']
        usermess=request.POST['umess']

        row=ContactForm.objects.create(Full_Name=username, Email_Address=useremail, Subject=usersub, Message=usermess)
        row.save()
    return render(request,'Contact Us.html')


# Below for Looping products from mysql in html page & fetches products and cart data for the current user

def product_list(request,category=None):
    if category == 'all' or not category:
        products = Products.objects.all()
        # print('the products are: ', products)
    else:
        products = Products.objects.filter(category=category)
        # print('the products are: ', products)


    cart_quantities = {}  # This will store the product quantities for the logged-in user

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        print('the cart items are',cart_items) # <QuerySet [<Cart: iPhone 16 Pro Max - Quantity: 1>, <Cart: Samsung Galaxy S24 Ultra - Quantity: 1>]> because of _str_
        for item in cart_items:
            cart_quantities[item.product.id] = item.quantity  # Map product id to quantity

    print('the cart quantities are',cart_quantities)  # {1: 1, 2: 1}

  # Dynamically decide which template to render
    if category == 'phone':
        template_name = 'Phones.html'
    elif category == 'watch':
        template_name = 'Watches.html'
    elif category == 'tablet':
        template_name = 'Tablets.html'
    else:
        template_name = 'Products.html'  # Default template for all items
    

    return render(request, template_name, {'products': products, 'cart_quantities': cart_quantities})

# below for Functionality

# Add to Cart
@login_required(login_url='login')  # Ensure the user is logged in before they can add to the cart
def add_to_cart(request, product_id):
    if request.method == 'POST':  # Ensure the form was submitted via POST
        product = get_object_or_404(Products, id=product_id)  # Get the product by ID, product_id getting from html loop, and giving as argument in html page as product.id
        print('the product is',product) #the product is iPhone 16 Pro Max   -> Because in Products table returing self.name
                                        #the product is Samsung Galaxy S24 Ultra

        # Try to get the cart item for the user and product, or create a new one if it doesn't exist
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        print('the cart_item is',cart_item) #the cart_item is iPhone 16 Pro Max - Quantity: 1 -> because in Cart tabel return f"{self.product.name} - Quantity: {self.quantity}"
                                            #the cart_item is Samsung Galaxy S24 Ultra - Quantity: 1
                                            # print(created) -> True for first time, if added again, then False

        if not created:  # If the cart item already exists
            cart_item.quantity += 1  # Increment the quantity by 1
            cart_item.save()  # Save the cart item to the database

         # Calculate the new subtotal for this product
        product_subtotal = cart_item.quantity * product.discount_price


        # If the request is an AJAX call (to avoid redirects)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return the updated quantity of the product in the cart
            return JsonResponse({'updated_quantity': cart_item.quantity if cart_item else 0, 'product_subtotal': product_subtotal, 'success': True}) #If cart_item exists, cart_item.quantity is returned. else 0
                                 #updated_quantity given in js

        # else:          # Fallback if the request is not AJAX 

        #     referer = request.META.get('HTTP_REFERER')
        #     if referer:
        #         parsed_url = urlparse(referer)
        #         if 'cart' in parsed_url.path:  # If the user came from the cart page
        #             return redirect('carts')
        #         else:  # If the user came from another page (e.g., products page)
        #             return HttpResponseRedirect(referer)
        #     else:
        #         # Default fallback if HTTP_REFERER is not available
        #         return redirect('product_list')

# Remove one quantity of a product from Cart
@login_required(login_url='login')  # Ensure the user is logged in before removing items from the cart
def remove_from_cart(request, product_id):
    if request.method == 'POST':  # Ensure the form was submitted via POST
        product = get_object_or_404(Products, id=product_id)  # Get the product by ID
        cart_item = Cart.objects.filter(user=request.user, product=product)  # Get the user's cart item
        print('cart are',cart_item)

        updated_quantity = 0  # Initialize updated quantity
        removed = False  # Initialize removed flag
        product_subtotal = 0  # Initialize product subtotal


        # if cart_item:  # If the item exists in the cart
        for item in cart_item:  # Iterate through each matching cart item
            if item.quantity > 1:  # If the quantity is more than 1, decrement it
                item.quantity -= 1
                item.save()
                updated_quantity = item.quantity
                 # Calculate the new subtotal for this product
                product_subtotal = item.quantity * product.discount_price

            else:  # If the quantity is 1, remove the item completely
                item.delete()
                updated_quantity = 0
                removed = True
                product_subtotal = 0

        

        # If the request is an AJAX call (to avoid redirects)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return the updated quantity of the product in the cart
            # return JsonResponse({'updated_quantity': item.quantity if cart_item else 0, 'success': True})
            return JsonResponse({'updated_quantity': updated_quantity, 'removed': removed, 'success': True, 'product_subtotal': product_subtotal})


        # else:          # Fallback if the request is not AJAX 

        #     referer = request.META.get('HTTP_REFERER')
        #     if referer:
        #         parsed_url = urlparse(referer)
        #         if 'cart' in parsed_url.path:  # If the user came from the cart page
        #             return redirect('carts')
        #         else:  # If the user came from another page (e.g., products page)
        #             return HttpResponseRedirect(referer)
        #     else:
        #         # Default fallback if HTTP_REFERER is not available
        #         return redirect('product_list')
            

    # If the method isn't POST, redirect to the product list
    return redirect('product_list')

# Remove all quantities of a specific product from Cart
@login_required(login_url='login')  # Ensure the user is logged in before removing all items
def remove_all_from_cart(request, product_id):
    if request.method == 'POST':  # Ensure the form was submitted via POST
        product = get_object_or_404(Products, id=product_id)  # Get the product by ID
        cart_item = get_object_or_404(Cart, user=request.user, product=product)  # Get the user's cart item

        cart_item.delete()  # Delete the cart item completely from the database
        return redirect('carts')  # Redirect to the cart page after removing the item
    else:
        return redirect('product_list')  # If the method isn't POST, redirect to the product list

# Clear the entire Cart
@login_required(login_url='login')
def clear_cart(request):
    if request.method == 'POST':  # Ensure the form was submitted via POST
        # Delete all cart items for the logged-in user
        Cart.objects.filter(user=request.user).delete()
        return redirect('carts')  # Redirect to the cart page after clearing the cart
    else:
        return redirect('product_list')  # If the method isn't POST, redirect to the product list

# Cart View
@login_required(login_url='login')  # Ensure the user is logged in before viewing the cart
def cart(request):
    # Get all cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate the subtotal for each cart item and add it as an attribute
    for item in cart_items:
        item.subtotal = item.quantity * item.product.discount_price # Store the subtotal as an attribute of each item

    
    # Ensure product data is fetched for each cart item
    # cart_items_with_products = []
    # for item in cart_items:
    #     # Add the product details to the cart item for easier access in the template
    #     item.product_details = item.product  # Ensure this is valid based on your Cart model

    # Calculate the total price by summing the total price of each cart item
    total_price = sum(item.total_price() for item in cart_items)


     # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'cart_total': total_price})

        
    # Render the cart template and pass the cart items and total price as context
    return render(request, 'Cart.html', {'cart_items': cart_items, 'cart_total': total_price})

# Below for login, logout and signup
def login_view(request):
    if request.method=='POST':
        user=authenticate(username=request.POST['uname'],password=request.POST['upassword'])
        if user is not None:
            login(request,user)
            return redirect('homes')
        else:
            messages.info(request,'invalid credentials')
            return render(request,'Login Page.html')

    return render(request,'Login Page.html')

def sign_up(request):
    if request.method=='POST':
        name=request.POST['uname']
        usermail=request.POST['uemail']
        password=request.POST['upassword']
        cpassword=request.POST['uconpass']

        if password==cpassword:
            if User.objects.filter(username=name).exists():
                messages.info(request,'account exists')
                return render(request,'SignUp Page.html')
            else:
                user=User.objects.create_user(username=name,password=password)
                login(request,user)
                messages.info(request,'account created successfully')
                return redirect('homes')
        else:
            messages.error(request,'passwords dont match')


    return render(request,'SignUp Page.html')

def logout_view(request):
    logout(request)
    return redirect('homes')

@login_required(login_url='login')  # Ensure the user is logged in before viewing the cart
def check_out(request):
    # Get all cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)

     # Calculate the subtotal for each cart item and add it as an attribute
    for item in cart_items:
        item.subtotal = item.quantity * item.product.discount_price # Store the subtotal as an attribute of each item

     # Check if the cart is empty
    if not cart_items.exists():
        # Add a pop-up message
        messages.warning(request, "Your cart is empty. Please add items before proceeding to checkout.")
        # Redirect to a suitable page, like the cart or homepage
        return render(request, 'Cart.html')  # Replace 'cart' with the URL name of your cart page
    
    # Calculate the total price
    total_price = sum(item.total_price() for item in cart_items)
    
    # Pass both cart items and total price to the template
    return render(request, 'Check Out.html', {'cart_items': cart_items, 'cart_total': total_price})

def payments_view(request):

     # Get all cart items for the logged-in user
    # cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate the total price
    # total_price = sum(item.total_price() for item in cart_items)

    # Process the order if the request method is POST
    if request.method == 'POST':
        usercontact = request.POST['mobile']
        useraddress = request.POST['address']
        username = request.POST['uname']
        useremail = request.POST['umail']
        usernote = request.POST['note']

        # Generate an 8-digit order ID
        order_id = random.randint(10000000, 99999999)

        # Generate order and delivery dates
        # date = dt.datetime.now()
        # bdate = date.strftime('%d-%m-%y & %H:%M:%S')
        cname = username
        cmail = useremail
        ccontact = usercontact
        caddress = useraddress
        cnote = usernote
        # pickup_date = date + dt.timedelta(days=7)
        # pdate = pickup_date.strftime('%d-%m-%y')
        # ddate = (pickup_date + dt.timedelta(days=15)).strftime('%d-%m-%y')

        # Prepare context data for the billing receipt
        data = {
            'orderid': order_id,
            # 'bdate': bdate,
            'cname': cname,
            'cemail': cmail,
            'cnumber': ccontact,
            'caddress': caddress,
            'cnote': cnote,
            # 'ddate': ddate,
            # 'cart_items': list(cart_items.values()),
            # 'cart_total': total_price
        }

        # Store user data in the session for later use
        request.session['billing_data'] = data

        return render(request, 'Payments.html')

    return render(request, 'Check Out.html')

@login_required(login_url='login')  # Ensure the user is logged in before viewing the cart
def billing(request):
    date = dt.datetime.now()
    bdate = date.strftime('%d-%m-%y & %H:%M:%S')
    pickup_date = date + dt.timedelta(days=7)
    pdate = pickup_date.strftime('%d-%m-%y')
    ddate = (pickup_date + dt.timedelta(days=15)).strftime('%d-%m-%y')


    # Get all cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
      # Calculate the subtotal for each cart item and add it as an attribute
    for item in cart_items:
        item.subtotal = item.quantity * item.product.discount_price # Store the subtotal as an attribute of each item
    
    # Calculate the total price
    total_price = sum(item.total_price() for item in cart_items)


     # Determine payment status based on query parameter
    payment_method = request.GET.get('payment', None)  # Get the 'payment' parameter from the URL
    # request.GET: This is a dictionary-like object in Django that contains all the key-value pairs from the query string in the URL.
    if payment_method == 'cod':
        payment_status = 'COD'
    else:
        payment_status = 'Paid Online'


     # Retrieve the stored data from the session
    user_data = request.session.get('billing_data', None)

    if user_data:
        user_data.update({           # Merge session data with additional data using .update
            'bdate': bdate,
            'pdate': pdate,
            'ddate': ddate,
            'cart_items': cart_items,
            'cart_total': total_price,
            'payment_status': payment_status,  # Add the dynamic payment status

        })
        # Render the billing receipt page
        response = render(request, 'Billing Receipt.html', user_data)

        # Clear session data after use
        request.session.pop('billing_data', None)

        return response

    

    # # Process the order if the request method is POST
    # if request.method == 'POST':
    #     usercontact = request.POST['mobile']
    #     useraddress = request.POST['address']
    #     username = request.POST['uname']
    #     useremail = request.POST['umail']
    #     usernote = request.POST['note']

    #     # Generate an 8-digit order ID
    #     order_id = random.randint(10000000, 99999999)

    #     # Generate order and delivery dates
    #     date = dt.datetime.now()
    #     bdate = date.strftime('%d-%m-%y & %H:%M:%S')
    #     cname = username
    #     cmail = useremail
    #     ccontact = usercontact
    #     caddress = useraddress
    #     cnote = usernote
    #     pickup_date = date + dt.timedelta(days=7)
    #     pdate = pickup_date.strftime('%d-%m-%y')
    #     ddate = (pickup_date + dt.timedelta(days=15)).strftime('%d-%m-%y')

    #     # Prepare context data for the billing receipt
    #     data = {
    #         'orderid': order_id,
    #         'bdate': bdate,
    #         'cname': cname,
    #         'cemail': cmail,
    #         'cnumber': ccontact,
    #         'caddress': caddress,
    #         'cnote': cnote,
    #         'ddate': ddate,
    #         'cart_items': cart_items,
    #         'cart_total': total_price
    #     }

    #     # If the cart is cleared and POST data exists, render the billing receipt
    #     return render(request, 'Billing Receipt.html', data)

    else:
        return render(request, 'Check Out.html')

@login_required(login_url='login')
def Billing_Clear_Cart(request):
    if request.method == 'POST':  # Ensure the form was submitted via POST
        # Delete all cart items for the logged-in user
        Cart.objects.filter(user=request.user).delete()
        return redirect('homes')  # Redirect to the cart page after clearing the cart
   
# Below for Search Results
def search_results(request):
    
    query = request.GET.get('query', '')  # Get the search query from the URL
    products = []
    cart_quantities = {}  # This will store the product quantities for the logged-in user


    if query:  # Check if the query is not empty
         # Split the query into individual keywords
        keywords = query.split()

        # Construct a dynamic OR filter for multiple keywords

        # helps you create OR conditions in queries
        search_filter = Q() # Initialize an empty Q object (acts as a placeholder).
        for i in keywords:
            search_filter |= Q(name__icontains=i)  # |=: This adds each new condition as an OR to the previous ones. 

        # Filter products where the name contains the query (case-insensitive)
        print('searched filters are: ',search_filter)  # (OR: ('name__icontains', 'samsung'), ('name__icontains', 'apple'), ('name__icontains', 'realme'))

        products = Products.objects.filter(search_filter)
        print("Filtered products:", products)  #<QuerySet [<Product: Samsung Galaxy S24 Ultra>, <Product: Samsung Tablet S10 Ultra>]>



        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
            print('the cart items are',cart_items) # <QuerySet [<Cart: iPhone 16 Pro Max - Quantity: 1>, <Cart: Samsung Galaxy S24 Ultra - Quantity: 1>]> because of _str_
            for item in cart_items:
                cart_quantities[item.product.id] = item.quantity  # Map product id to quantity

    return render(request, 'Search Results.html', {'query': query, 'products': products, 'cart_quantities': cart_quantities})