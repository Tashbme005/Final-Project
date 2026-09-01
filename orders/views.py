from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order

# Create your views here.
@login_required
def ordersPage(request):
    orders = Order.objects.all()
    return render(request, "orders/orders.html", {"orders": orders})

@login_required
def create_order(request):
    if request.method == 'POST':
        order_name = request.POST.get('order_name')
        order_date = request.POST.get('order_date')
        order_status = request.POST.get('order_status')

        new_order = Order(
            order_name=order_name,
            order_date=order_date,
            order_status=order_status
        )
        new_order.save()
        return redirect('ordersPage')
    return render(request, 'orders/order_form.html')


@login_required
def order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'orders/view_order.html', {'order': order})

@login_required
def update_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        order_name = request.POST.get('order_name')
        order_date = request.POST.get('order_date')
        order_status = request.POST.get('order_status')

        order.order_name = order_name
        order.order_date = order_date
        order.order_status = order_status
        order.save()
        return redirect('ordersPage')
    return render(request, 'orders/order_form.html', {'order': order})

@login_required
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect('ordersPage')

@login_required
def create_customer(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')

        new_customer = Customer(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone
        )
        new_customer.save()
        return redirect('ordersPage')
    return render(request, 'orders/customer_form.html')

def create_vehicle(request):
        if request.method == 'POST':
            vehicle_make = request.POST.get('vehicle_make')
            vehicle_model = request.POST.get('vehicle_model')
            vehicle_year = request.POST.get('vehicle_year')

            new_vehicle = Vehicle(
                vehicle_make=vehicle_make,
                vehicle_model=vehicle_model,
                vehicle_year=vehicle_year
            )
            new_vehicle.save()
            return redirect('ordersPage')
        return render(request, 'orders/vehicle_form.html')

def create_inspection(request):
    if request.method == 'POST':
        inspection_date = request.POST.get('inspection_date')
        inspection_result = request.POST.get('inspection_result')

        new_inspection = Inspection(
            inspection_date=inspection_date,
            inspection_result=inspection_result
        )
        new_inspection.save()
        return redirect('ordersPage')
    return render(request, 'orders/inspection_form.html')

def add_order(request):
    if request.method == 'POST':
        payload = request.POST
        form = OrderForm(payload)
        if form.is_valid():
            form.save()
            return redirect('ordersPage')
    return render(request, 'orders/order_form.html', {'form': OrderForm()})

def add_customer(request):
    if request.method == 'POST':
        payload = request.POST
        form = CustomerForm(payload)
        if form.is_valid():
            form.save()
            return redirect('ordersPage')
    return render(request, 'orders/customer_form.html', {'form': CustomerForm()})

def add_vehicle(request):
    if request.method == 'POST':
        payload = request.POST
        form = VehicleForm(payload)
        if form.is_valid():
            form.save()
            return redirect('ordersPage')
    return render(request, 'orders/vehicle_form.html', {'form': VehicleForm()})

def add_inspection(request):
    if request.method == 'POST':
        payload = request.POST
        form = InspectionForm(payload)
        if form.is_valid():
            form.save()
            return redirect('ordersPage')
    return render(request, 'orders/inspection_form.html', {'form': InspectionForm()})

def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'orders/customer_details.html', {'customer': customer})

def vehicle_details(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    return render(request, 'orders/vehicle_details.html', {'vehicle': vehicle}) 

def inspection_details(request, inspection_id):
    inspection = Inspection.objects.get(id=inspection_id)
    return render(request, 'orders/inspection_details.html', {'inspection': inspection})

def update_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        customer.customer_name = request.POST.get('customer_name')
        customer.customer_email = request.POST.get('customer_email')
        customer.customer_phone = request.POST.get('customer_phone')
        customer.save()
        return redirect('ordersPage')
    return render(request, 'orders/customer_form.html', {'customer': customer})

def update_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    if request.method == 'POST':
        vehicle.vehicle_make = request.POST.get('vehicle_make')
        vehicle.vehicle_model = request.POST.get('vehicle_model')
        vehicle.vehicle_year = request.POST.get('vehicle_year')
        vehicle.save()
        return redirect('ordersPage')
    return render(request, 'orders/vehicle_form.html', {'vehicle': vehicle})

def update_inspection(request, inspection_id):
    inspection = Inspection.objects.get(id=inspection_id)
    if request.method == 'POST':
        inspection.inspection_date = request.POST.get('inspection_date')
        inspection.inspection_result = request.POST.get('inspection_result')
        inspection.save()
        return redirect('ordersPage')
    return render(request, 'orders/inspection_form.html', {'inspection': inspection})   

def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('ordersPage')

def delete_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    return redirect('ordersPage')

def delete_inspection(request, inspection_id):
    inspection = Inspection.objects.get(id=inspection_id)
    inspection.delete()
    return redirect('ordersPage')

