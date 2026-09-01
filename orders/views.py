from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from employees.access import role_required, ADMIN, SENIOR, TECHNICIAN, user_role
from payments.models import Payment
from .models import Customer, Vehicle, Inspection, Order
from .forms import CustomerForm, VehicleForm, InspectionForm, OrderForm


def _form_initial(request, *fields):
    initial = {}
    for field in fields:
        value = request.GET.get(field)
        if value:
            initial[field] = value
    return initial


@role_required(ADMIN, SENIOR)
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'orders/customer_list.html', {'customers': customers})


@role_required(ADMIN, SENIOR)
def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer saved. You can add their vehicle next.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'orders/simple_form.html', {
        'form': form,
        'title': 'Register Customer',
        'cancel_url': 'customer_list',
    })


@role_required(ADMIN, SENIOR)
def vehicle_list(request):
    vehicles = Vehicle.objects.select_related('customer').all()
    return render(request, 'orders/vehicle_list.html', {'vehicles': vehicles})


@role_required(ADMIN, SENIOR)
def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle saved. You can inspect it or open a job card next.')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(initial=_form_initial(request, 'customer'))
    return render(request, 'orders/simple_form.html', {
        'form': form,
        'title': 'Register Vehicle',
        'cancel_url': 'vehicle_list',
    })


@role_required(ADMIN, SENIOR)
def inspection_list(request):
    inspections = Inspection.objects.select_related('vehicle').order_by('-done_at')
    return render(request, 'orders/inspection_list.html', {'inspections': inspections})


@role_required(ADMIN, SENIOR)
def inspection_add(request):
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inspection saved. Request parts or open a job card next.')
            return redirect('inspection_list')
    else:
        form = InspectionForm(initial=_form_initial(request, 'vehicle'))
    return render(request, 'orders/simple_form.html', {
        'form': form,
        'title': 'Senior Technician Inspection',
        'note': 'The senior technician records the parts and oils this car needs.',
        'cancel_url': 'inspection_list',
    })


@role_required(ADMIN, SENIOR, TECHNICIAN)
def order_list(request):
    orders = Order.objects.select_related('vehicle', 'vehicle__customer').prefetch_related('service', 'technicians').order_by('-created_at')
    employee = getattr(request.user, 'employee', None)
    if user_role(request.user) == TECHNICIAN and employee:
        orders = orders.filter(technicians=employee)
    status_filter = request.GET.get('status')
    allowed = {choice[0] for choice in Order.STATUS_CHOICES}
    if status_filter in allowed:
        orders = orders.filter(status=status_filter)
    else:
        status_filter = ''
    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'status_filter': status_filter,
    })


@role_required(ADMIN, SENIOR)
def order_add(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job card saved.')
            return redirect('order_list')
    else:
        form = OrderForm(initial=_form_initial(request, 'vehicle'))
    return render(request, 'orders/simple_form.html', {
        'form': form,
        'title': 'New Job Card',
        'note': 'A car can have one or more services. One or more technicians can handle the job.',
        'cancel_url': 'order_list',
    })


@role_required(ADMIN, SENIOR, TECHNICIAN)
def order_detail(request, order_id):
    orders = Order.objects.select_related('vehicle', 'vehicle__customer').prefetch_related('service', 'technicians')
    employee = getattr(request.user, 'employee', None)
    if user_role(request.user) == TECHNICIAN and employee:
        orders = orders.filter(technicians=employee)
    order = get_object_or_404(orders, pk=order_id)
    payment = Payment.objects.filter(order=order).first()
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'payment': payment,
    })


@role_required(ADMIN, SENIOR)
@require_POST
def order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    messages.success(request, 'Job card deleted.')
    return redirect('order_list')
