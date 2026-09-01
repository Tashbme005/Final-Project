from django.db import models
from employees.models import Employee


class Part(models.Model):
    part_id = models.AutoField(primary_key=True)
    part_name = models.CharField(max_length=100, unique=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.part_name


class PartsRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Issued', 'Issued'),
    ]
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True)
    requested_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='parts_requested')
    issued_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parts_issued',
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.part.part_name} x{self.quantity}"
