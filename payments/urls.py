from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('add/', views.payment_add, name='payment_add'),
    path('receipt/<int:payment_id>/', views.receipt_view, name='receipt_view'),
]
