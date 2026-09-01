from django.contrib import admin
from .models import Customer, Vehicle, Inspection, Order

# Register your models here.
admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Inspection)
admin.site.register(Order)