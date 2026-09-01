from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from employees.access import role_required, ADMIN, SENIOR, TECHNICIAN, user_role
from .models import Part, PartsRequest
from .forms import PartForm, PartsRequestForm


@role_required(ADMIN, SENIOR, TECHNICIAN)
def part_list(request):
    employee = getattr(request.user, 'employee', None)
    if user_role(request.user) == TECHNICIAN and employee:
        issued = PartsRequest.objects.filter(
            issued_to=employee,
            status='Issued',
        ).select_related('part', 'requested_by').order_by('-requested_at')
        return render(request, 'inventory/part_list.html', {
            'parts': [],
            'requests': issued,
            'issued_only': True,
        })
    parts = Part.objects.all()
    requests = PartsRequest.objects.select_related('part', 'requested_by', 'issued_to').order_by('-requested_at')[:10]
    return render(request, 'inventory/part_list.html', {
        'parts': parts,
        'requests': requests,
        'issued_only': False,
    })


@role_required(ADMIN)
def part_add(request):
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Part saved.')
            return redirect('part_list')
    else:
        form = PartForm()
    return render(request, 'inventory/part_form.html', {'form': form, 'title': 'Add Part'})


@role_required(ADMIN)
def part_edit(request, part_id):
    part = get_object_or_404(Part, pk=part_id)
    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            messages.success(request, 'Part updated.')
            return redirect('part_list')
    else:
        form = PartForm(instance=part)
    return render(request, 'inventory/part_form.html', {'form': form, 'title': 'Edit Part'})


@role_required(ADMIN)
@require_POST
def part_delete(request, part_id):
    part = get_object_or_404(Part, pk=part_id)
    part.delete()
    messages.success(request, 'Part deleted.')
    return redirect('part_list')


@role_required(ADMIN, SENIOR)
def part_request_add(request):
    if request.method == 'POST':
        form = PartsRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parts request saved.')
            return redirect('part_list')
    else:
        form = PartsRequestForm()
    return render(request, 'inventory/part_form.html', {
        'form': form,
        'title': 'Request Parts for a Job',
        'note': 'Senior technician selects the oils and filters the owner should buy.',
    })
