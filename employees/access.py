from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

ADMIN = 'admin'
SENIOR = 'senior'
TECHNICIAN = 'technician'


def user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return ADMIN
    employee = getattr(user, 'employee', None)
    if employee:
        return employee.job_role
    return None


def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if user_role(request.user) not in roles:
                messages.error(request, 'You are not allowed to open that page.')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
