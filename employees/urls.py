from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("employees_list/", views.employees, name="employees"),
    path("employee_form/", views.create_employee, name="create_employee"),
    path("update_employee/<int:employee_id>/", views.update_employee, name="update_employee"),
    path("delete_employee/<int:employee_id>/", views.delete_employee, name="delete_employee"),
]