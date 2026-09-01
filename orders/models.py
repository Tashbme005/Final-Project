from django.db import models
from services.models import Service
from employees.models import Employee, Role


# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=15)
    customer_email = models.EmailField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.customer_name


class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle_id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=20, choices=[('Heavy', 'Heavy'), ('Commercial', 'Commercial'), ('Small', 'Small')])
    car_model = models.CharField(max_length=50, blank=True)
    number_plate = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.number_plate} - {self.car_model}"

class Inspection(models.Model):
    inspection_id = models.AutoField(primary_key=True)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    findings = models.CharField(max_length=100)
    recommended_service = models.CharField(max_length=50)
    done_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    order_id = models.AutoField(primary_key=True, unique=True)
    role = models.ManyToManyField(Role)
    service = models.ManyToManyField("services.Service")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.vehicle.number_plate}"


