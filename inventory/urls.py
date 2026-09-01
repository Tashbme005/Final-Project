from django.urls import path
from . import views

urlpatterns = [
    path('', views.part_list, name='part_list'),
    path('add/', views.part_add, name='part_add'),
    path('<int:part_id>/edit/', views.part_edit, name='part_edit'),
    path('<int:part_id>/delete/', views.part_delete, name='part_delete'),
    path('request/', views.part_request_add, name='part_request_add'),
]
