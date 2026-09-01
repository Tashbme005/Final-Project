from datetime import date
from decimal import Decimal
from django.test import Client, TestCase
from django.urls import reverse
from employees.models import Employee
from employees.test_helpers import login_as_admin
from services.models import Service
from .models import Customer, Vehicle, Inspection, Order


class OrderTests(TestCase):
    def setUp(self):
        login_as_admin(self.client)
        self.customer = Customer.objects.create(
            customer_name='Catherine Mazzi',
            customer_email='cath@gmail.com',
            phone_number='0772001122',
        )
        self.vehicle = Vehicle.objects.create(
            customer=self.customer,
            size='Small',
            car_model='Toyota Corolla',
            number_plate='UAA 123A',
        )
        self.tech1 = Employee.objects.create(
            employee_name='Mary Nakato',
            date_of_birth=date(1992, 7, 21),
            phone_number='0751987654',
            email='mary.nakato@oasbay.ug',
            nin='CF920721002DEF',
        )
        self.tech2 = Employee.objects.create(
            employee_name='Peter Okello',
            date_of_birth=date(1990, 11, 5),
            phone_number='0703112233',
            email='peter.okello@oasbay.ug',
            nin='CM901105003GHI',
        )
        self.labour = Service.objects.create(
            service_name='Labour charge',
            description='Standard bay labour',
            unit_cost=Decimal('20000'),
        )
        self.alignment = Service.objects.create(
            service_name='Wheel alignment',
            description='Wheel alignment for one car',
            unit_cost=Decimal('30000'),
        )

    def test_customer_and_vehicle_are_saved(self):
        self.assertEqual(str(self.customer), 'Catherine Mazzi')
        self.assertEqual(str(self.vehicle), 'UAA 123A (Toyota Corolla)')
        self.assertEqual(self.vehicle.size, 'Small')

    def test_vehicle_sizes_match_the_bay(self):
        sizes = [choice[0] for choice in Vehicle.SIZE_CHOICES]
        self.assertEqual(sizes, ['Heavy', 'Commercial', 'Small'])

    def test_senior_technician_can_record_an_inspection(self):
        inspection = Inspection.objects.create(
            vehicle=self.vehicle,
            findings='Brake pads worn out',
            recommended_service='Brake pad replacement',
        )
        self.assertEqual(inspection.vehicle, self.vehicle)
        self.assertIn('Brake pads', inspection.findings)

    def test_a_job_can_have_more_than_one_service_and_technician(self):
        order = Order.objects.create(
            vehicle=self.vehicle,
            description='Customer requested a full service checkup',
        )
        order.service.add(self.labour, self.alignment)
        order.technicians.add(self.tech1, self.tech2)

        self.assertEqual(order.service.count(), 2)
        self.assertEqual(order.technicians.count(), 2)
        self.assertEqual(order.service_total(), Decimal('50000'))
        self.assertEqual(order.status, 'Pending')

    def test_order_pages_open(self):
        order = Order.objects.create(vehicle=self.vehicle)
        pages = [
            reverse('customer_list'),
            reverse('customer_add'),
            reverse('vehicle_list'),
            reverse('vehicle_add'),
            reverse('inspection_list'),
            reverse('inspection_add'),
            reverse('order_list'),
            reverse('order_add'),
            reverse('order_detail', args=[order.order_id]),
        ]
        for url in pages:
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_customer_can_be_registered_from_the_form(self):
        response = self.client.post(reverse('customer_add'), {
            'customer_name': 'John Mukasa',
            'customer_email': 'john.mukasa@email.com',
            'phone_number': '0777001122',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(customer_email='john.mukasa@email.com').exists())

    def test_apostrophe_in_a_customer_name_is_saved_as_plain_text(self):
        response = self.client.post(reverse('customer_add'), {
            'customer_name': "Catherine O'Brien",
            'customer_email': 'cath.obrien@email.com',
            'phone_number': '0772003344',
        })
        self.assertEqual(response.status_code, 302)
        saved = Customer.objects.get(customer_email='cath.obrien@email.com')
        self.assertEqual(saved.customer_name, "Catherine O'Brien")
        self.assertEqual(Customer.objects.count(), 2)
        self.assertTrue(Vehicle.objects.filter(number_plate='UAA 123A').exists())

    def test_empty_customer_form_shows_error_messages(self):
        response = self.client.post(reverse('customer_add'), {
            'customer_name': '',
            'customer_email': '',
            'phone_number': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter the customer full name.')
        self.assertContains(response, 'Enter the customer phone number.')
        self.assertEqual(Customer.objects.count(), 1)

    def test_invalid_customer_defaults_are_rejected(self):
        response = self.client.post(reverse('customer_add'), {
            'customer_name': 'John',
            'customer_email': 'not-an-email',
            'phone_number': '12345',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a first name and a last name.')
        self.assertContains(response, 'Enter a valid Ugandan phone number')
        self.assertFalse(Customer.objects.filter(customer_name='John').exists())

    def test_html_in_a_customer_name_is_escaped_on_the_page(self):
        Customer.objects.create(
            customer_name='<b>Jane Doe</b>',
            customer_email='jane.markup@email.com',
            phone_number='0772112233',
        )
        response = self.client.get(reverse('customer_list'))
        self.assertContains(response, '&lt;b&gt;Jane Doe&lt;/b&gt;')
        self.assertNotContains(response, '<b>Jane Doe</b>')

    def test_delete_job_card_requires_post(self):
        order = Order.objects.create(vehicle=self.vehicle)
        response = self.client.get(reverse('order_delete', args=[order.order_id]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Order.objects.filter(pk=order.order_id).exists())

    def test_customer_form_post_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse('customer_add'), {
            'customer_name': 'John Mukasa',
            'customer_email': 'john.csrf@email.com',
            'phone_number': '0777001122',
        })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Customer.objects.filter(customer_email='john.csrf@email.com').exists())

    def test_forms_link_back_to_their_own_list(self):
        customer_form = self.client.get(reverse('customer_add'))
        self.assertContains(customer_form, f'href="{reverse("customer_list")}"')
        self.assertContains(customer_form, 'Back')
        vehicle_form = self.client.get(reverse('vehicle_add'))
        self.assertContains(vehicle_form, f'href="{reverse("vehicle_list")}"')
        inspection_form = self.client.get(reverse('inspection_add'))
        self.assertContains(inspection_form, f'href="{reverse("inspection_list")}"')

    def test_job_list_can_filter_by_status(self):
        Order.objects.create(vehicle=self.vehicle, status='Pending')
        done_vehicle = Vehicle.objects.create(
            customer=self.customer,
            size='Small',
            car_model='Hiace',
            number_plate='UBB 456B',
        )
        Order.objects.create(vehicle=done_vehicle, status='Completed')
        page = self.client.get(reverse('order_list'), {'status': 'Completed'})
        self.assertContains(page, 'UBB 456B')
        self.assertNotContains(page, 'UAA 123A')

    def test_vehicle_form_can_start_with_a_customer_selected(self):
        page = self.client.get(reverse('vehicle_add'), {'customer': self.customer.customer_id})
        self.assertContains(page, f'value="{self.customer.customer_id}"')
        self.assertContains(page, 'selected')
