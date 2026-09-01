from django.db import models

# Create your models here.
class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=50)
    description = models.TextField()
    unit_cost = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.service_name







