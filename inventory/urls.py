from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventoryPage, name="inventoryPage"),
    path("add/", views.index, name="index"),
    path("part_form.html/", views.create_part, name="create_part"),
    path("view_part.html/<int:part_id>/", views.view_part, name="view_part"),
    path("parts_request_form.html/", views.part_request, name="part_request"),
    path("part_request_details/<int:part_request_id>/", views.part_request_details, name="part_request_details"),
    path("delete_part/<int:part_id>/", views.delete_part, name="delete_part"),
    path("delete_part_request/<int:part_request_id>/", views.delete_part_request, name="delete_part_request"),
    path("update_part/<int:part_id>/", views.update_part, name="update_part"),
    path("oas/inventory/tests.py", views.tests, name="tests"),

]