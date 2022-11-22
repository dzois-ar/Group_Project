
from django.core.mail import message, send_mail
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . forms import UserCustomerForm
from django.core.paginator import Paginator
from django.db.models import Q

#Search 
def search(request):
    query = request.GET.get('query', '')
    data = cartData(request)
    cartItems = data['cartItems']
    products= Product.objects.filter(Q(type__icontains=query) | Q(brand__icontains=query) | Q(price__icontains=query) | Q(color__icontains=query) | Q(sex__icontains=query) )
    return render(request, 'eshop/customer_user.html', {'products': products, 'query': query, 'cartItems':cartItems })

#Eshop-Products list-Pagination
def eshop(request):
   products_list=Product.objects.all()
   # Set up Pagination
   p = Paginator(Product.objects.all(), 6)

   page = request.GET.get('page')
   products = p.get_page(page)
   nums="a" * products.paginator.num_pages

   context={'products':products, 'products_list': products_list, 'page': page, 'nums':nums}
   return render(request, 'eshop/eshop.html', context)

#User login
def login_user(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('eshop:customer_user')
        else:
            if not username:
                errors['empty_username'] = 'Please enter username'
            elif not password:
                errors['empty_password'] = 'Please enter password'
            elif user is None:
                errors['invalid'] = 'Username and password do not match'
    
    return render(request, 'eshop/login.html', errors)

#User Logout
def logout(request):
    return render(request, 'eshop/logout.html', {})

#Customer products, additions to cart
@login_required(login_url='/eshop/login/')
def customer_user(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    products_list=Product.objects.all()
    # Set up Pagination
    p = Paginator(Product.objects.all(), 6)
  
    page = request.GET.get('page')
    products = p.get_page(page)
    nums="a" * products.paginator.num_pages
    
    context={'products':products, 'cartItems':cartItems,'products_list': products_list, 'page': page, 'nums':nums}
    return render(request, 'eshop/customer_user.html', context)

#Cart
@login_required(login_url='/eshop/login/') 
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'eshop/cart.html', context)

#Checkout
@login_required(login_url='/eshop/login/')
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'eshop/checkout.html', context)

#Update item from cart 
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)

#Transaction-Payment
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment complete', safe=False)

#view product(eshop.html)
def view_product(request, id):
    product_object = Product.objects.get(id=id)
    return render(request, 'eshop/view_product.html', {'product_object':product_object})

#view product for customer(customer_user.html)
@login_required(login_url='/eshop/login/')
def view_product_log(request, id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(id=id)
    context={'product':product, 'cartItems':cartItems }
    return render(request, 'eshop/view_product_log.html', context)

#Customer Sign Up in connection with forms.py
def customer_registration(request):
    customer_form=UserCustomerForm(request.POST)
    if customer_form.is_valid():
        customer_form.save()
        email = customer_form.cleaned_data.get('email')
        name = customer_form.cleaned_data.get('name')
        username = customer_form.cleaned_data.get('username')
        password = customer_form.cleaned_data.get('password1')
        user = User.objects.get(username=username)
        customer=Customer(user=user, email=email,name=name)
        customer.save()
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return HttpResponseRedirect('/eshop/login')
    else:
        customer_form = UserCustomerForm()

    return render(request, 
            'eshop/customer_registration.html', {'form': customer_form})

#Filters(Mens-Womens) for eshop.html
#This function is a filter and choose (Hoodies-Male) products
def mens_hoodies_list_base_page(request):
    products=Product.objects.filter(type='Hoodies',sex='Male')
    context={'products':products}
    return render(request,'eshop/eshop.html',context)

#This function is a filter and choose (Tshirt-Male) products
def mens_tshirt_list_base_page(request): 
    products=Product.objects.filter(type='Tshirt',sex='Male')
    context={'products':products}
    return render(request,'eshop/eshop.html',context)

#This function is a filter and choose (Jean-Male) products
def mens_jean_list_base_page(request):
    products=Product.objects.filter(type='Jean',sex='Male')
    context={'products':products}
    return render(request,'eshop/eshop.html',context)

#This function is a filter and choose (Coat-Male) products
def mens_coat_list_base_page(request):
    products=Product.objects.filter(type='Coat',sex='Male')
    context={'products':products}
    return render(request,'eshop/eshop.html',context)

#This function is a filter and choose (Hoodies-Women) products
def women_hoodies_list_base_page(request):
    products=Product.objects.filter(type='Hoodies',sex='Women')
    context={'products':products}
    return render(request,'eshop/eshop.html',context)

#This function is a filter and choose (Tshirt-Women) products
def women_tshirt_list_base_page(request):
    products=Product.objects.filter(type='Tshirt',sex='Women')
    context={'products':products}
    return render(request,'eshop/eshop.html',context)

#This function is a filter and choose (Jean-Women)products
def women_jean_list_base_page(request):
    products=Product.objects.filter(type='Jean',sex='Women')
    context={'products':products}
    return render(request,'eshop/eshop.html',context)

#This function is a filter and choose (Coat-Women)products
def women_coat_list_base_page(request):
    products=Product.objects.filter(type='Coat',sex='Women')
    context={'products':products,}
    return render(request,'eshop/eshop.html',context)

#Filters(Mens-Womens) for customer.html
#This function is a filter and choose (Hoodies-Male) products
@login_required(login_url='/eshop/login/')
def mens_hoodies_list(request):
    data = cartData(request)

    cartItems = data['cartItems']
    products=Product.objects.filter(type='Hoodies',sex='Male')
    context={'products':products,'cartItems':cartItems }
    return render(request,'eshop/customer_user.html',context)

#This function is a filter and choose (Tshirt-Male) products
@login_required(login_url='/eshop/login/')
def mens_tshirt_list(request):
    data = cartData(request)

    cartItems = data['cartItems']
    products=Product.objects.filter(type='Tshirt',sex='Male')
    context={'products':products,'cartItems':cartItems}
    return render(request,'eshop/customer_user.html',context)

#This function is a filter and choose (Jean-Male) products
@login_required(login_url='/eshop/login/')
def mens_jean_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products=Product.objects.filter(type='Jean',sex='Male')
    context={'products':products, 'cartItems':cartItems}
    return render(request,'eshop/customer_user.html',context)

#This function is a filter and choose (Coat-Male) products
@login_required(login_url='/eshop/login/')
def mens_coat_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products=Product.objects.filter(type='Coat',sex='Male')
    context={'products':products,'cartItems':cartItems}
    return render(request,'eshop/customer_user.html',context)

#This function is a filter and choose (Hoodies-Women) products
@login_required(login_url='/eshop/login/')
def women_hoodies_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products=Product.objects.filter(type='Hoodies',sex='Women')
    context={'products':products, 'cartItems':cartItems}
    return render(request,'eshop/customer_user.html',context)

#This function is a filter and choose (Tshirt-Women) products
@login_required(login_url='/eshop/login/')
def women_tshirt_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products=Product.objects.filter(type='Tshirt',sex='Women')
    context={'products':products, 'cartItems':cartItems}
    return render(request,'eshop/customer_user.html',context)

#This function is a filter and choose (Jean-Women)products
@login_required(login_url='/eshop/login/')
def women_jean_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products=Product.objects.filter(type='Jean',sex='Women')
    context={'products':products, 'cartItems':cartItems}
    return render(request,'eshop/customer_user.html',context)

#This function is a filter and choose (Coat-Women)products
@login_required(login_url='/eshop/login/')
def women_coat_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products=Product.objects.filter(type='Coat',sex='Women')
    context={'products':products, 'cartItems':cartItems}
    return render(request,'eshop/customer_user.html',context)

















