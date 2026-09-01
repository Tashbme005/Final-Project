from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Service

# Create your views here.
@login_required
def service(request):
    services = Service.objects.all()
    return render(request, "services/services.html", {"services": services})

@login_required
def create_service(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        description = request.POST.get('description')
        unit_cost = request.POST.get('unit_cost')

        new_service = Service(
            service_name=service_name,
            description=description,
            unit_cost=unit_cost
        )
        new_service.save()
        return redirect('services') 

    return render(request, 'services/service_form.html')

@login_required
def service_details(request, service_id):
    service = Service.objects.get(pk=service_id)
    return render(request, 'services/view_service.html', {'service': service})

@login_required
def update_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        description = request.POST.get('description')
        unit_cost = request.POST.get('unit_cost')

        service.service_name = service_name
        service.description = description
        service.unit_cost = unit_cost
        service.save()
        return redirect('services') 

    return render(request, 'services/service_form.html', {'service': service})

@login_required
def delete_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    service.delete()
    return redirect('services')

