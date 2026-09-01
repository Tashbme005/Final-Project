from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Oyera Auto Service Bay"
admin.site.site_title = "OAS Bay"
admin.site.index_title = "Records management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employees.urls')),
    path('services/', include('services.urls')),
    path('inventory/', include('inventory.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
]
