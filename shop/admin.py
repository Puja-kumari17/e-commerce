from django.contrib import admin
from .models import Product, Order, Contact, ReturnRequest
from .models import Product, Order, Contact, ReturnRequest, Cart

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(ReturnRequest)
admin.site.register(Cart)