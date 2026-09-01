from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee, Role


# Create your views here.
def index(request):
    index = Employee.objects.all()
    return render(request, "employees/index.html")

@login_required
def employees(request):
    employees = Employee.objects.all()
    return render(request, "employees/employees_list.html", {"employees": employees})


@login_required
def create_employee(request):
    if request.method == 'POST':
       employee_name = request.POST.get('employee_name')
       date_of_birth = request.POST.get('date_of_birth')
       phone_number = request.POST.get('phone_number')
       email = request.POST.get('email')
       nin = request.POST.get('nin')
       passport_number = request.POST.get('passport_number')

       new_employee = Employee(
           employee_name=employee_name,
           date_of_birth=date_of_birth,
           phone_number=phone_number,
           email=email,
           nin=nin,
           passport_number=passport_number,
       )
       new_employee.save()
       return redirect('employees') 

    return render(request, 'employees/employee_form.html')


@login_required
def add_employee(request):
    if request.method == 'POST':
        payload = request.POST
        form = EmployeeForm(payload)
        if form.is_valid():
            form.save()
            return redirect('employees')
    return render(request, 'employees/employee_form.html', {'form': EmployeeForm()})


@login_required
def employee_details(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    return render(request, 'employees/view_employee.html', {'employee': employee})

@login_required
def update_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})


@login_required
def delete_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    employee.delete()
    return redirect('employees')

@login_required
def employee_roles(request):
    roles = Role.objects.all()
    return render(request, "employees/employee_roles.html", {"roles": roles})   

@login_required
def create_role(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        role = request.POST.get('role')
        description = request.POST.get('description')

        employee = Employee.objects.get(pk=employee_id)

        new_role = Role(
            employee=employee,
            role=role,
            description=description
        )
        new_role.save()
        return redirect('employee_roles') 

    employees = Employee.objects.all()
    return render(request, 'employees/role_form.html', {'employees': employees})

@login_required
def update_role(request, role_id):
    role = Role.objects.get(pk=role_id)
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        role_name = request.POST.get('role')
        description = request.POST.get('description')

        employee = Employee.objects.get(pk=employee_id)

        role.employee = employee
        role.role = role_name
        role.description = description
        role.save()
        return redirect('employee_roles') 

    employees = Employee.objects.all()
    return render(request, 'employees/role_form.html', {'role': role, 'employees': employees})  

def delete_role(request, role_id):
    role = Role.objects.get(pk=role_id)
    role.delete()
    return redirect('employee_roles')

@login_required
def role_details(request, role_id):
    role = Role.objects.get(pk=role_id)
    return render(request, 'employees/view_role.html', {'role': role})  


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            employee = Employee.objects.get(email=email)
            employee.password = new_password
            employee.save()
            return redirect('index')  # Redirect to a success page or login page
        except Employee.DoesNotExist:
            error_message = "No employee found with the provided email."
            return render(request, 'employees/password_reset.html', {'error_message': error_message})

    return render(request, 'employees/password.html')
