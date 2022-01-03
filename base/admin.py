from django.contrib import admin

from base.models import Address, Category, Customer, Medicine, Order, OrderItem, Prescription, covid

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(Medicine)
admin.site.register(covid)
admin.site.register(Prescription)
admin.site.register(OrderItem)