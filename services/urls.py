from django.urls import path
from . import views

urlpatterns = [
    path("", views.service, name="service"),
    path("service_form.html/", views.create_service, name="create_service"),
    path("view_service.html/<int:service_id>/", views.service_details, name="service_details"),
    path("update_service/<int:service_id>/", views.update_service, name="update_service"),
    path("delete_service/<int:service_id>/", views.delete_service, name="delete_service"),
]