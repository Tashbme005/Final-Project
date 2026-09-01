from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True, auto_created=True)
    employee_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=False)
    phone_number = models.CharField(max_length=10, null=False)
    email = models.EmailField(max_length=30, unique=True)
    nin = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=128, blank=True)

    def __str__(self):
       return self.employee_name

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    description = models.TextField()

