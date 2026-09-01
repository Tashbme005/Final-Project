from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .access import role_required, ADMIN, SENIOR, TECHNICIAN, user_role
from .models import Employee, Role
from .forms import EmployeeForm, RoleForm
from orders.models import Customer, Vehicle, Order
from inventory.models import Part
from services.models import Service
from payments.models import Payment


def _login_next(request):
    return request.POST.get('next') or request.GET.get('next') or ''


def render_login(request):
    if request.user.is_authenticated:
        next_url = _login_next(request)
        if next_url.startswith('/'):
            return redirect(next_url)
        return redirect('home')
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        user = authenticate(request, username=username, password=password)
        if user is None:
            from django.contrib.auth.models import User
            match = User.objects.filter(email__iexact=username).first()
            if match:
                user = authenticate(request, username=match.username, password=password)
        if user is not None:
            login(request, user)
            next_url = _login_next(request)
            if next_url.startswith('/'):
                return redirect(next_url)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'employees/login.html', {'next': _login_next(request)})


def login_view(request):
    if request.method != 'POST':
        query = request.GET.urlencode()
        return redirect(f'/{("?" + query) if query else ""}')
    return render_login(request)


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def home(request):
    if not request.user.is_authenticated:
        return render_login(request)
    role = user_role(request.user)
    employee = getattr(request.user, 'employee', None)
    orders = Order.objects.all()
    if role == TECHNICIAN and employee:
        orders = orders.filter(technicians=employee)
        recent_orders = orders.select_related('vehicle', 'vehicle__customer').order_by('-created_at')[:8]
        context = {
            'technician_count': 1,
            'customer_count': orders.values('vehicle__customer').distinct().count(),
            'vehicle_count': orders.values('vehicle').distinct().count(),
            'order_count': orders.count(),
            'pending_count': orders.filter(status='Pending').count(),
            'in_progress_count': orders.filter(status='In Progress').count(),
            'completed_count': orders.filter(status='Completed').count(),
            'part_count': 0,
            'service_count': 0,
            'payment_count': Payment.objects.filter(order__technicians=employee).count(),
            'recent_orders': recent_orders,
        }
        return render(request, 'employees/index.html', context)
    recent_orders = Order.objects.select_related('vehicle', 'vehicle__customer').order_by('-created_at')[:8]
    context = {
        'technician_count': Employee.objects.count(),
        'customer_count': Customer.objects.count(),
        'vehicle_count': Vehicle.objects.count(),
        'order_count': Order.objects.count(),
        'pending_count': Order.objects.filter(status='Pending').count(),
        'in_progress_count': Order.objects.filter(status='In Progress').count(),
        'completed_count': Order.objects.filter(status='Completed').count(),
        'part_count': Part.objects.count(),
        'service_count': Service.objects.count(),
        'payment_count': Payment.objects.count(),
        'recent_orders': recent_orders,
    }
    return render(request, 'employees/index.html', context)


@role_required(ADMIN)
def employee_list(request):
    employees = Employee.objects.prefetch_related('role_set').all()
    extra_roles = Role.objects.select_related('employee').order_by('role')
    return render(request, 'employees/employees_list.html', {
        'employees': employees,
        'extra_roles': extra_roles,
    })


@role_required(ADMIN)
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member saved.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Staff Member'})


@role_required(ADMIN)
def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member updated.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Staff Member'})


@role_required(ADMIN)
@require_POST
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
    messages.success(request, 'Staff member deleted.')
    return redirect('employee_list')


def _form_initial(request, *fields):
    initial = {}
    for field in fields:
        value = request.GET.get(field)
        if value:
            initial[field] = value
    return initial


@role_required(ADMIN)
def role_add(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job role saved.')
            return redirect('employee_list')
    else:
        form = RoleForm(initial=_form_initial(request, 'employee'))
    return render(request, 'employees/role_form.html', {
        'form': form,
        'title': 'Add Job Role',
        'note': 'Give a staff member another work title at the bay. Login access still follows Admin, Senior technician or Technician.',
    })


@role_required(ADMIN)
@require_POST
def role_delete(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    role.delete()
    messages.success(request, 'Job role deleted.')
    return redirect('employee_list')
