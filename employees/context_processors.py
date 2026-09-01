from .access import user_role, ADMIN, SENIOR, TECHNICIAN


def staff_role(request):
    role = user_role(request.user)
    employee = getattr(request.user, 'employee', None) if request.user.is_authenticated else None
    profile_name = ''
    profile_initial = ''
    role_label = ''
    if request.user.is_authenticated:
        profile_name = employee.employee_name if employee else request.user.get_username()
        profile_initial = (profile_name[:1] or 'S').upper()
        if employee:
            role_label = employee.get_job_role_display()
        elif role == ADMIN:
            role_label = 'Admin'
        else:
            role_label = 'Staff'
    return {
        'staff_role': role,
        'is_admin': role == ADMIN,
        'is_senior': role == SENIOR,
        'is_technician': role == TECHNICIAN,
        'can_manage_customers': role in (ADMIN, SENIOR),
        'can_inspect': role in (ADMIN, SENIOR),
        'can_manage_jobs': role in (ADMIN, SENIOR),
        'can_view_jobs': role in (ADMIN, SENIOR, TECHNICIAN),
        'can_view_services': role in (ADMIN, SENIOR),
        'can_manage_services': role == ADMIN,
        'can_view_parts': role in (ADMIN, SENIOR, TECHNICIAN),
        'can_manage_parts': role == ADMIN,
        'can_request_parts': role in (ADMIN, SENIOR),
        'can_manage_payments': role == ADMIN,
        'can_view_receipts': role in (ADMIN, SENIOR, TECHNICIAN),
        'can_manage_staff': role == ADMIN,
        'profile_name': profile_name,
        'profile_initial': profile_initial,
        'role_label': role_label,
    }
