from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from employees.access import role_required, ADMIN, SENIOR
from .models import Service
from .forms import ServiceForm


@role_required(ADMIN, SENIOR)
def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})


@role_required(ADMIN)
def service_add(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service saved.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Add Service'})


@role_required(ADMIN)
def service_edit(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service'})


@role_required(ADMIN)
@require_POST
def service_delete(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    service.delete()
    messages.success(request, 'Service deleted.')
    return redirect('service_list')
