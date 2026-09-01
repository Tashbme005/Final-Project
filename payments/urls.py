from django.urls import path
from . import views

urlpatterns = [
    path("", views.paymentPage, name="paymentPage"),
    path("payment_form.html/", views.create_payment, name="create_payment"),
    path("receipt_form.html/", views.create_receipt, name="create_receipt"),
    path("payment.html/<int:payment_id>/", views.total_payment_amount, name="total_payment_amount"),
]