from django.urls import path
from . import views

urlpatterns= [ 
    path('', views.store,name="store"), #frontpage
    path('cart/', views.cart,name="cart"), # for carts
    path('checkout/', views.checkout,name="checkout"), #for checkout
    
    path('update_item/', views.updateItem,name="update_item"),

    path('process_order/', views.processOrder,name="process_order"),  


]

