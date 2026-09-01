from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.order_add, name='order_add'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_add, name='vehicle_add'),
    path('inspections/', views.inspection_list, name='inspection_list'),
    path('inspections/add/', views.inspection_add, name='inspection_add'),
]
