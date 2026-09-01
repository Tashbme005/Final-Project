from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('staff/', views.employee_list, name='employee_list'),
    path('staff/add/', views.employee_add, name='employee_add'),
    path('staff/<int:employee_id>/edit/', views.employee_edit, name='employee_edit'),
    path('staff/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),
    path('staff/roles/add/', views.role_add, name='role_add'),
    path('staff/roles/<int:role_id>/delete/', views.role_delete, name='role_delete'),
]
