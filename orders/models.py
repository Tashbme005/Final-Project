from django.db import models
from employees.models import Employee, Role


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=80)
    customer_email = models.EmailField(max_length=80, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.customer_name


class Vehicle(models.Model):
    SIZE_CHOICES = [
        ('Heavy', 'Heavy'),
        ('Commercial', 'Commercial'),
        ('Small', 'Small'),
    ]
    vehicle_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    car_model = models.CharField(max_length=50, blank=True)
    number_plate = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.number_plate} ({self.car_model})"


class Inspection(models.Model):
    inspection_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    findings = models.CharField(max_length=200)
    recommended_service = models.CharField(max_length=100)
    done_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection {self.inspection_id} - {self.vehicle.number_plate}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    order_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role, blank=True)
    technicians = models.ManyToManyField(Employee, blank=True)
    service = models.ManyToManyField('services.Service', blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.order_id} - {self.vehicle.number_plate}"

    def service_total(self):
        total = 0
        for item in self.service.all():
            total += item.unit_cost
        return total
