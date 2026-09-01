from django.db import models
from orders.models import Order


# Create your models here.
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, unique=True)
    order = models.OneToOneField(Order, on_delete=models.RESTRICT)
    payment_status = models.CharField(max_length=20, choices=[('Paid','Paid'), ('Pending', 'Pending'), ('Terminated', 'Terminated')])
    payment_method = models.CharField(max_length=10, choices=[('Card', 'Card'), ('Cash', 'Cash')])
    amount_paid = models.DecimalField(max_digits=20, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.payment_status}"


class Receipt(models.Model):
    receipt_id = models.AutoField(primary_key=True, unique=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    receipt_number = models.CharField(max_length=20, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipt_number