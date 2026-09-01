from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Employee, Role
from .test_helpers import login_as_admin
from orders.models import Customer, Vehicle, Order


class EmployeeTests(TestCase):
    def setUp(self):
        login_as_admin(self.client)
    def test_citizen_staff_can_be_saved_with_nin(self):
        employee = Employee.objects.create(
            employee_name='Shatrah Ddamulira',
            date_of_birth=date(1999, 1, 1),
            phone_number='0771234567',
            email='shatrah@gmail.com',
            nin='CF123456789CXF',
        )
        self.assertEqual(str(employee), 'Shatrah Ddamulira')
        self.assertEqual(employee.nin, 'CF123456789CXF')
        self.assertEqual(employee.passport_number, '')

    def test_foreign_staff_can_be_saved_with_passport(self):
        employee = Employee.objects.create(
            employee_name='Mary Jane',
            date_of_birth=date(1999, 1, 1),
            phone_number='0771234567',
            email='mary@gmail.com',
            has_nin=False,
            nin='',
            passport_number='A12345678',
        )
        self.assertEqual(employee.passport_number, 'A12345678')

    def test_role_is_linked_to_an_employee(self):
        employee = Employee.objects.create(
            employee_name='James Oyera',
            date_of_birth=date(1984, 3, 12),
            phone_number='0772123456',
            email='james.oyera@oasbay.ug',
            nin='CM840312001ABC',
        )
        role = Role.objects.create(
            employee=employee,
            role='Senior Technician',
            description='Inspects cars and lists parts needed',
        )
        self.assertEqual(str(role), 'James Oyera Senior Technician')
        self.assertEqual(employee.role_set.count(), 1)

    def test_dashboard_and_staff_pages_open(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('employee_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('employee_add')).status_code, 200)
        self.assertEqual(self.client.get(reverse('role_add')).status_code, 200)

    def test_navbar_shows_profile_and_logout(self):
        page = self.client.get(reverse('home'))
        self.assertContains(page, 'class="profile-chip"')
        self.assertContains(page, 'class="logout-btn"')
        self.assertContains(page, 'Logout')
        self.assertContains(page, 'admin')
        self.assertContains(page, 'Admin')
        self.assertContains(page, 'employees/logo.png')
        self.assertContains(page, 'employees/favicon-32.png')

    def test_another_job_role_can_be_added_from_the_form(self):
        employee = Employee.objects.create(
            employee_name='Mary Nakato',
            date_of_birth=date(1992, 7, 21),
            phone_number='0751987654',
            email='mary.role@oasbay.ug',
            nin='CF920721002DEF',
        )
        response = self.client.post(reverse('role_add'), {
            'employee': employee.employee_id,
            'role': 'Alignment specialist',
            'description': 'Handles wheel alignment and balance',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Role.objects.filter(employee=employee, role='Alignment specialist').exists())
        staff_page = self.client.get(reverse('employee_list'))
        self.assertContains(staff_page, 'Alignment specialist')

    def test_empty_job_role_form_shows_error_messages(self):
        response = self.client.post(reverse('role_add'), {
            'employee': '',
            'role': '',
            'description': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select the staff member for this job role.')
        self.assertContains(response, 'Enter the job role title.')
        self.assertEqual(Role.objects.count(), 0)

    def test_staff_can_be_added_from_the_form(self):
        response = self.client.post(reverse('employee_add'), {
            'employee_name': 'Peter Okello',
            'date_of_birth': '1990-11-05',
            'phone_number': '0703112233',
            'email': 'peter.okello@oasbay.ug',
            'nin': 'CM901105003GHI',
            'passport_number': '',
            'id_kind': 'yes',
            'job_role': 'technician',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Employee.objects.filter(email='peter.okello@oasbay.ug').exists())

    def test_apostrophe_in_a_name_is_saved_as_plain_text(self):
        response = self.client.post(reverse('employee_add'), {
            'employee_name': "O'Connor Ddamulira",
            'date_of_birth': '1995-06-18',
            'phone_number': '0782000001',
            'email': 'oconnor@oasbay.ug',
            'nin': 'CM950618004MNO',
            'passport_number': '',
            'id_kind': 'yes',
            'job_role': 'technician',
        })
        self.assertEqual(response.status_code, 302)
        saved = Employee.objects.get(email='oconnor@oasbay.ug')
        self.assertEqual(saved.employee_name, "O'Connor Ddamulira")
        self.assertEqual(Employee.objects.count(), 1)

    def test_empty_staff_form_shows_error_messages(self):
        response = self.client.post(reverse('employee_add'), {
            'employee_name': '',
            'date_of_birth': '',
            'phone_number': '',
            'email': '',
            'nin': '',
            'passport_number': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter the staff member full name.')
        self.assertContains(response, 'Enter a phone number.')
        self.assertEqual(Employee.objects.count(), 0)

    def test_spaces_and_one_name_are_rejected(self):
        response = self.client.post(reverse('employee_add'), {
            'employee_name': '   ',
            'date_of_birth': '1990-11-05',
            'phone_number': '123',
            'email': 'not-an-email',
            'nin': '##',
            'passport_number': '',
            'id_kind': 'yes',
            'job_role': 'technician',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter the staff member full name.')
        self.assertEqual(Employee.objects.count(), 0)

    def test_foreigner_form_requires_passport_not_nin(self):
        response = self.client.post(reverse('employee_add'), {
            'employee_name': 'Mary Jane',
            'date_of_birth': '1999-01-01',
            'phone_number': '0771234567',
            'email': 'mary.jane@oasbay.ug',
            'id_kind': 'no',
            'job_role': 'technician',
            'nin': '',
            'passport_number': 'A12345678',
        })
        self.assertEqual(response.status_code, 302)
        saved = Employee.objects.get(email='mary.jane@oasbay.ug')
        self.assertFalse(saved.has_nin)
        self.assertEqual(saved.nin, '')
        self.assertEqual(saved.passport_number, 'A12345678')

    def test_foreigner_without_passport_is_rejected(self):
        response = self.client.post(reverse('employee_add'), {
            'employee_name': 'Mary Jane',
            'date_of_birth': '1999-01-01',
            'phone_number': '0771234567',
            'email': 'mary.none@oasbay.ug',
            'id_kind': 'no',
            'job_role': 'technician',
            'nin': '',
            'passport_number': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passport number is required.')
        self.assertFalse(Employee.objects.filter(email='mary.none@oasbay.ug').exists())


class AccessTests(TestCase):
    def test_login_page_is_visible(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Staff login')
        self.assertContains(response, 'auth-slider')
        self.assertContains(response, 'auth-overlay')
        self.assertNotContains(response, 'carousel-indicators')
        self.assertContains(response, 'employees/auth/nairobi-garage.jpg')
        self.assertContains(response, 'Developed by Shatrah Ddamulira')
        self.assertContains(response, 'data-username="admin"')
        self.assertContains(response, 'data-username="james"')
        self.assertContains(response, 'data-username="mary"')
        self.assertContains(response, 'employees/favicon-32.png')
        self.assertNotContains(response, 'Customers')

    def test_old_login_url_opens_root(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_home_requires_login(self):
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/?next='))
        self.assertNotIn('/login/', response.url)

    def test_technician_cannot_open_staff_payments_or_services(self):
        user = User.objects.create_user('mary', password='tech-pass-123')
        Employee.objects.create(
            user=user,
            employee_name='Mary Nakato',
            date_of_birth=date(1992, 7, 21),
            phone_number='0751987654',
            email='mary.nakato@oasbay.ug',
            job_role=Employee.ROLE_TECHNICIAN,
            nin='CF920721002DEF',
        )
        self.client.login(username='mary', password='tech-pass-123')
        self.assertEqual(self.client.get(reverse('employee_list')).status_code, 302)
        self.assertEqual(self.client.get(reverse('role_add')).status_code, 302)
        self.assertEqual(self.client.get(reverse('payment_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('payment_add')).status_code, 302)
        self.assertEqual(self.client.get(reverse('service_list')).status_code, 302)
        self.assertEqual(self.client.get(reverse('customer_list')).status_code, 302)
        self.assertEqual(self.client.get(reverse('order_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('part_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('part_request_add')).status_code, 302)
        self.assertEqual(self.client.get(reverse('part_add')).status_code, 302)

    def test_technician_only_sees_assigned_jobs(self):
        user = User.objects.create_user('tech', password='tech-pass-123')
        employee = Employee.objects.create(
            user=user,
            employee_name='Mary Nakato',
            date_of_birth=date(1992, 7, 21),
            phone_number='0751987654',
            email='mary.jobs@oasbay.ug',
            job_role=Employee.ROLE_TECHNICIAN,
            nin='CF920721002DEF',
        )
        owner = Customer.objects.create(
            customer_name='John Mukasa',
            customer_email='john.jobs@email.com',
            phone_number='0777001122',
        )
        mine_vehicle = Vehicle.objects.create(customer=owner, size='Small', car_model='Premio', number_plate='UAX 123A')
        other_vehicle = Vehicle.objects.create(customer=owner, size='Small', car_model='Hiace', number_plate='UBB 456B')
        mine = Order.objects.create(vehicle=mine_vehicle, description='My job')
        mine.technicians.add(employee)
        other = Order.objects.create(vehicle=other_vehicle, description='Someone else')
        self.client.login(username='tech', password='tech-pass-123')
        jobs = self.client.get(reverse('order_list'))
        self.assertContains(jobs, 'UAX 123A')
        self.assertNotContains(jobs, 'UBB 456B')
        self.assertEqual(self.client.get(reverse('order_detail', args=[mine.order_id])).status_code, 200)
        self.assertEqual(self.client.get(reverse('order_detail', args=[other.order_id])).status_code, 404)

    def test_senior_can_inspect_view_services_and_request_parts_but_cannot_add_them(self):
        user = User.objects.create_user('james', password='senior-pass-123')
        Employee.objects.create(
            user=user,
            employee_name='James Oyera',
            date_of_birth=date(1984, 3, 12),
            phone_number='0772123456',
            email='james.oyera@oasbay.ug',
            job_role=Employee.ROLE_SENIOR,
            nin='CM840312001ABC',
        )
        self.client.login(username='james', password='senior-pass-123')
        self.assertEqual(self.client.get(reverse('inspection_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('inspection_add')).status_code, 200)
        services_page = self.client.get(reverse('service_list'))
        self.assertEqual(services_page.status_code, 200)
        self.assertNotContains(services_page, 'Add service')
        self.assertEqual(self.client.get(reverse('order_add')).status_code, 200)
        self.assertEqual(self.client.get(reverse('part_request_add')).status_code, 200)
        self.assertEqual(self.client.get(reverse('service_add')).status_code, 302)
        self.assertEqual(self.client.get(reverse('part_add')).status_code, 302)
        self.assertEqual(self.client.get(reverse('employee_list')).status_code, 302)


class DeploySettingsTests(TestCase):
    def test_static_files_use_an_absolute_url(self):
        from django.conf import settings
        self.assertTrue(settings.STATIC_URL.startswith('/'))
        self.assertTrue(str(settings.STATIC_ROOT).endswith('staticfiles'))

    def test_postgres_url_is_parsed_for_vercel(self):
        from oas.settings import postgres_from_url
        config = postgres_from_url(
            'postgres://bay:p%40ss@db.example.com:5432/oasbay?sslmode=require'
        )
        self.assertEqual(config['ENGINE'], 'django.db.backends.postgresql')
        self.assertEqual(config['NAME'], 'oasbay')
        self.assertEqual(config['USER'], 'bay')
        self.assertEqual(config['PASSWORD'], 'p@ss')
        self.assertEqual(config['HOST'], 'db.example.com')
        self.assertEqual(config['PORT'], '5432')
        self.assertEqual(config['OPTIONS']['sslmode'], 'require')
