from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField #importing djangos default user model
# Create your models here.

#customer model
class Customer(models.Model): #we build out customer model that inherit from Model
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) #customer will have one to one relation ship with user ie user will have only 1 customer and viceversa
    #on_delete=models.CASCADE customer gets deleted if user item gets deleted
    #null=True store null value in DB, blank determines whether field will be req in form, blank=true, field will not be req, if false field cannot be blank
    name = models.CharField(max_length=200, null=True) #string value
    email = models.CharField(max_length=200, null=True) 

    def __str__(self):
        return self.name

#product model
class Product(models.Model):
    name = models.CharField(max_length=200, null=True) #string value
    price= models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False) #BY DEFAULT ALL ITEMS IN OUR CART WILL BE PHYSICAL ITEMS, but it changes if he item is digital
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property  #so that even if our products dont have any images, there is no error
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=" "
        return url

class Order(models.Model): #cart
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    #customer will have one to many relationship with order, cuz 1 customer can have many orders
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, null=True,blank=False)
    #if complete is false, then it is open cart and we can add more item t the cart
    transaction_id = models.CharField(max_length=200, null=True)
    #usique id for our order
    #image

    def __str__(self):
        return str(self.id)
    
    @property #shipping method that loops through all our shipping item, and checks if out item is physical or digital. If digital=Fasle, then it needs to ship those items.
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self): #total for the cart value
        orderitems = self.orderitem_set.all() #get the orderitems
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self): #total for our no of items in our cart
        orderitems = self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

    

class OrderItem(models.Model): #items need to added to the order with many to 1 relationship, many items, 1 order
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True, blank=True) #1 cart having multiple order item
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self): #to calculate total=no of items*price
        total=self.product.price*self.quantity #go to product class get price value and mult with quantity
        return total
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True) #even if order gets deleted, then well have shipping address of that customer
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address