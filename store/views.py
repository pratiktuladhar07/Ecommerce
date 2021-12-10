from django.shortcuts import render
from django.http import JsonResponse #just to send a message
import json

import datetime

from .models import *

# Create your views here.
def store(request):
	if request.user.is_authenticated: #checking if user has logged i  or not
		customer= request.user.customer #access 1to1 relationship between user and customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)              #we want to create an order or get an order that exists
		#we are creating an object or querying into one
		items=order.orderitem_set.all() #get all the order items that have this oreder(parent.child_set.all())
		cartItems = order.get_cart_items #for the red dot on carts
	else:
		items=[]
		order={'get_cart_total' : 0, 'get_cart_items':0,'shipping':False}
		cartItems=order['get_cart_items']

	products=Product.objects.all() #querying all of the products(get all the products)
	context = {'products' : products,'cartItems' : cartItems} #passing them into our template
	return render(request, 'store/store.html', context) #reflecting on our frontend

def cart(request):

	if request.user.is_authenticated: #checking if user has logged i  or not
		customer= request.user.customer #access 1to1 relationship between user and customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)   #we want to create an order or get an order that exists
		#we are creating an object or querying into one
		items=order.orderitem_set.all() #get all the order items that have this oreder(parent.child_set.all())
		cartItems = order.get_cart_items
	else:
		items=[]
		order={'get_cart_total' : 0, 'get_cart_items':0,'shipping':False}
		cartItems=order['get_cart_items']
	context = {'items' : items, 'order' : order,'cartItems' : cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated: #checking if user has logged i  or not
		customer= request.user.customer #access 1to1 relationship between user and customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)              #we want to create an order or get an order that exists
		#we are creating an object or querying into one
		items=order.orderitem_set.all() #get all the order items that have this oreder(parent.child_set.all())
		cartItems = order.get_cart_items
	else:
		items=[]
		order={'get_cart_total' : 0, 'get_cart_items':0,'shipping':False}
		cartItems=order['get_cart_items']
	context = {'items' : items, 'order' : order,'cartItems' : cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request): #whatever happends in the backend, when add to cart button is pressed
	data = json.loads(request.body) #to print data, we use import of json, .load- parse the data(that was in string value) into dict
	productId=data['productId']  #we get some values
	action=data['action']
	print("Action:", action)
	print("Product:", productId)

	customer = request.user.customer #to query the customer
	product = Product.objects.get(id=productId) #to get the product that we are passing in
	order, created = Order.objects.get_or_create(customer=customer,complete=False) #get or create a order attached to the customer
	orderItem, created = OrderItem.objects.get_or_create(order=order,product=product) #get_or_create so we can change the quantity of items(add or subtract)
	
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()


	return JsonResponse("item Added", safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request): #view for our post request to send data do, process orders in backend
	#print('Data:', request.body)
	
	transaction_id=datetime.datetime.now().timestamp()
	if request.user.is_authenticated:
		customer=request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False) #get oredr, if not create it,we set the customer, we need order that has vaue of complete=false
		data = json.loads(request.body) #parse the data and access it
		total=float(data['form']['total'])
		order.transaction_id=transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save() #we match to see if cart total== total we sent here.

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer, #everything from ShippingAddress model
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
	

	else:
		print("user not logged in")
	return JsonResponse("paymwnt complete....",safe=False)
