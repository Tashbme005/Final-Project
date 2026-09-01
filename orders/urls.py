from django.urls import path
from . import views

urlpatterns = [
    path("", views.ordersPage, name="ordersPage"),
    path("customer_form.html/", views.create_customer, name="create_customer"),
    path("vehicle_form.html/", views.create_vehicle, name="create_vehicle"),
    path("inspection_form.html/", views.create_inspection, name="create_inspection"),
    path("create_order/", views.create_order, name="create_order"),
    path("order_details/<int:order_id>/", views.order_details, name="order_details"),
    path("update_order/<int:order_id>/", views.update_order, name="update_order"),
    path("delete_order/<int:order_id>/", views.delete_order, name="delete_order"),
]