from django.db import models
from employees.models import Employee


# Create your models here.
class Part(models.Model):
    part_id = models.AutoField(primary_key=True)
    part_name = models.CharField(max_length=100, unique=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.part_name


class PartsRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Issued", "Issued"),
    ]
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True)
    requested_by = models.ForeignKey(Employee, on_delete=models.PROTECT)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")