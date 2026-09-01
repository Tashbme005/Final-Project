from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_SENIOR = 'senior'
    ROLE_TECHNICIAN = 'technician'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_SENIOR, 'Senior Technician'),
        (ROLE_TECHNICIAN, 'Technician'),
    ]

    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')
    employee_name = models.CharField(max_length=80)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=80, unique=True)
    job_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_TECHNICIAN)
    has_nin = models.BooleanField(default=True)
    nin = models.CharField(max_length=20, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.employee_name


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=40)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.employee_name} {self.role}"
