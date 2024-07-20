from django.contrib import admin
from .models import Booking, Category, MenuItem, Order, OrderItem, Cart, Menu

admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(Menu)
