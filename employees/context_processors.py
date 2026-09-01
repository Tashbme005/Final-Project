from .access import user_role, ADMIN, SENIOR, TECHNICIAN


def staff_role(request):
    role = user_role(request.user)
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
    }
