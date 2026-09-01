from django.core.management.base import BaseCommand
from datetime import date
from django.contrib.auth.models import User
from employees.models import Employee, Role
from services.models import Service
from inventory.models import Part, PartsRequest
from orders.models import Customer, Vehicle, Inspection, Order
from payments.models import Payment, Receipt


def attach_login(username, password, employee=None, job_role=Employee.ROLE_TECHNICIAN, is_superuser=False):
    user, _created = User.objects.get_or_create(
        username=username,
        defaults={'email': employee.email if employee else f'{username}@oasbay.ug'},
    )
    if employee:
        user.email = employee.email
    user.is_staff = is_superuser
    user.is_superuser = is_superuser
    user.set_password(password)
    user.save()
    if employee:
        employee.user = user
        employee.job_role = job_role
        employee.save()
    return user


class Command(BaseCommand):
    help = 'Load sample OAS Bay records'

    def handle(self, *args, **options):
        if not Service.objects.exists():
            self.load_records()
        self.ensure_logins()
        self.ensure_issued_parts()
        self.stdout.write(self.style.SUCCESS('Sample records and login accounts are ready.'))
        self.stdout.write('Login at /  admin/OasAdmin1  james/OasSenior1  mary/OasTech1')

    def ensure_logins(self):
        attach_login('admin', 'OasAdmin1', is_superuser=True)
        james = Employee.objects.filter(email='james.oyera@oasbay.ug').first()
        mary = Employee.objects.filter(email='mary.nakato@oasbay.ug').first()
        peter = Employee.objects.filter(email='peter.okello@oasbay.ug').first()
        if james:
            attach_login('james', 'OasSenior1', james, Employee.ROLE_SENIOR)
        if mary:
            attach_login('mary', 'OasTech1', mary, Employee.ROLE_TECHNICIAN)
        if peter:
            attach_login('peter', 'OasTech1', peter, Employee.ROLE_TECHNICIAN)

    def ensure_issued_parts(self):
        mary = Employee.objects.filter(email='mary.nakato@oasbay.ug').first()
        james = Employee.objects.filter(email='james.oyera@oasbay.ug').first()
        oil = Part.objects.filter(part_name='Oil filter').first()
        if mary and james and oil and not PartsRequest.objects.filter(issued_to=mary).exists():
            PartsRequest.objects.create(
                part=oil,
                quantity=1,
                comment='Issued for Premio oil service',
                requested_by=james,
                issued_to=mary,
                status='Issued',
            )

    def load_records(self):
        senior = Employee.objects.create(
            employee_name='James Oyera',
            date_of_birth=date(1984, 3, 12),
            phone_number='0772123456',
            email='james.oyera@oasbay.ug',
            job_role=Employee.ROLE_SENIOR,
            nin='CM840312001ABC',
        )
        tech1 = Employee.objects.create(
            employee_name='Mary Nakato',
            date_of_birth=date(1992, 7, 21),
            phone_number='0751987654',
            email='mary.nakato@oasbay.ug',
            job_role=Employee.ROLE_TECHNICIAN,
            nin='CF920721002DEF',
        )
        tech2 = Employee.objects.create(
            employee_name='Peter Okello',
            date_of_birth=date(1990, 11, 5),
            phone_number='0703112233',
            email='peter.okello@oasbay.ug',
            job_role=Employee.ROLE_TECHNICIAN,
            nin='CM901105003GHI',
        )
        Role.objects.create(employee=senior, role='Senior Technician', description='Inspects cars and lists parts needed')
        Role.objects.create(employee=tech1, role='Technician', description='Handles oil, filters and brakes')
        Role.objects.create(employee=tech2, role='Technician', description='Handles alignment and balance')

        labour = Service.objects.create(service_name='Labour charge', description='Standard bay labour after parts are bought', unit_cost=20000)
        alignment = Service.objects.create(service_name='Wheel alignment', description='Wheel alignment for one car', unit_cost=30000)
        balance = Service.objects.create(service_name='Wheel balance', description='Wheel balance for one car', unit_cost=20000)
        oil_change = Service.objects.create(service_name='Engine oil and filter service', description='Drain old oil, fit new filter and refill', unit_cost=20000)
        brakes = Service.objects.create(service_name='Brake pads and fluid', description='Replace pads and top up brake fluid', unit_cost=20000)
        greasing = Service.objects.create(service_name='Greasing', description='Minor greasing service', unit_cost=20000)

        Part.objects.create(part_name='Engine oil 5L (small cars)', quantity_in_stock=24, unit_price=79000)
        Part.objects.create(part_name='Engine oil 10L (heavy / commercial)', quantity_in_stock=12, unit_price=200000)
        Part.objects.create(part_name='Gearbox oil', quantity_in_stock=15, unit_price=85000)
        Part.objects.create(part_name='Brake fluid', quantity_in_stock=30, unit_price=15000)
        Part.objects.create(part_name='Oil filter', quantity_in_stock=40, unit_price=18000)
        Part.objects.create(part_name='Gearbox filter', quantity_in_stock=18, unit_price=20000)
        Part.objects.create(part_name='Brake pads', quantity_in_stock=20, unit_price=45000)
        Part.objects.create(part_name='Grease', quantity_in_stock=25, unit_price=12000)

        c1 = Customer.objects.create(customer_name='John Mukasa', customer_email='john.mukasa@email.com', phone_number='0777001122')
        c2 = Customer.objects.create(customer_name='Aisha Nambi', customer_email='aisha.nambi@email.com', phone_number='0755003344')
        c3 = Customer.objects.create(customer_name='David Otim', customer_email='david.otim@email.com', phone_number='0704005566')

        v1 = Vehicle.objects.create(customer=c1, size='Small', car_model='Toyota Premio', number_plate='UAX 123A')
        v2 = Vehicle.objects.create(customer=c2, size='Commercial', car_model='Toyota Hiace', number_plate='UBB 456B')
        v3 = Vehicle.objects.create(customer=c3, size='Heavy', car_model='Isuzu FVR', number_plate='UAE 789C')

        Inspection.objects.create(vehicle=v1, findings='Old engine oil and dirty filter', recommended_service='Engine oil, oil filter and labour')
        Inspection.objects.create(vehicle=v2, findings='Uneven tyre wear', recommended_service='Wheel alignment and balance')
        Inspection.objects.create(vehicle=v3, findings='Soft brakes', recommended_service='Brake pads, brake fluid and labour')

        o1 = Order.objects.create(vehicle=v1, description='Oil service after owner bought 5L oil and a filter', status='Completed')
        o1.service.add(oil_change, labour)
        o1.technicians.add(tech1)

        PartsRequest.objects.create(
            part=Part.objects.get(part_name='Oil filter'),
            quantity=1,
            comment='Issued for Premio oil service',
            requested_by=senior,
            issued_to=tech1,
            status='Issued',
        )

        o2 = Order.objects.create(vehicle=v2, description='Alignment and balance', status='In Progress')
        o2.service.add(alignment, balance)
        o2.technicians.add(tech2, tech1)

        o3 = Order.objects.create(vehicle=v3, description='Brake work', status='Pending')
        o3.service.add(brakes, greasing)
        o3.technicians.add(senior, tech1)

        payment = Payment.objects.create(order=o1, payment_status='Paid', payment_method='Cash', amount_paid=o1.service_total(), comment='Owner already bought oil and filter')
        Receipt.objects.create(payment=payment, receipt_number='OAS0001')
