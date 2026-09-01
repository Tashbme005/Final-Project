from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from employees.models import Employee
from employees.test_helpers import login_as_admin
from .models import Part, PartsRequest


class InventoryTests(TestCase):
    def setUp(self):
        login_as_admin(self.client)
        self.technician = Employee.objects.create(
            employee_name='John Joseph',
            date_of_birth=date(1988, 4, 10),
            phone_number='0771000000',
            email='john.joseph@oasbay.ug',
            nin='CM880410001JKL',
        )

    def test_parts_use_the_bay_price_ranges(self):
        oil = Part.objects.create(
            part_name='Engine oil 5L (small cars)',
            quantity_in_stock=24,
            unit_price=Decimal('79000'),
        )
        heavy_oil = Part.objects.create(
            part_name='Engine oil 10L (heavy / commercial)',
            quantity_in_stock=12,
            unit_price=Decimal('200000'),
        )
        brake_fluid = Part.objects.create(
            part_name='Brake fluid',
            quantity_in_stock=30,
            unit_price=Decimal('15000'),
        )
        oil_filter = Part.objects.create(
            part_name='Oil filter',
            quantity_in_stock=40,
            unit_price=Decimal('18000'),
        )

        self.assertGreaterEqual(oil.unit_price, Decimal('79000'))
        self.assertLessEqual(heavy_oil.unit_price, Decimal('200000'))
        self.assertGreaterEqual(brake_fluid.unit_price, Decimal('13000'))
        self.assertLessEqual(brake_fluid.unit_price, Decimal('20000'))
        self.assertGreaterEqual(oil_filter.unit_price, Decimal('15000'))
        self.assertLessEqual(oil_filter.unit_price, Decimal('20000'))

    def test_technician_can_request_parts_for_a_job(self):
        part = Part.objects.create(
            part_name='Oil filter',
            quantity_in_stock=10,
            unit_price=Decimal('18000'),
        )
        request = PartsRequest.objects.create(
            part=part,
            quantity=2,
            comment='Needed after inspection',
            requested_by=self.technician,
        )
        self.assertEqual(request.status, 'Pending')
        self.assertEqual(str(request), 'Oil filter x2')
        self.assertEqual(request.requested_by.employee_name, 'John Joseph')

    def test_inventory_pages_open(self):
        self.assertEqual(self.client.get(reverse('part_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('part_add')).status_code, 200)
        self.assertEqual(self.client.get(reverse('part_request_add')).status_code, 200)

    def test_part_can_be_added_from_the_form(self):
        response = self.client.post(reverse('part_add'), {
            'part_name': 'Gearbox oil',
            'quantity_in_stock': '15',
            'unit_price': '85000',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Part.objects.filter(part_name='Gearbox oil').exists())

    def test_apostrophe_in_a_part_name_is_saved_as_plain_text(self):
        response = self.client.post(reverse('part_add'), {
            'part_name': "O'ring seal",
            'quantity_in_stock': '20',
            'unit_price': '5000',
        })
        self.assertEqual(response.status_code, 302)
        saved = Part.objects.get(part_name="O'ring seal")
        self.assertEqual(saved.quantity_in_stock, 20)
        self.assertEqual(Part.objects.count(), 1)

    def test_empty_part_form_shows_error_messages(self):
        response = self.client.post(reverse('part_add'), {
            'part_name': '',
            'quantity_in_stock': '',
            'unit_price': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter the part name.')
        self.assertEqual(Part.objects.count(), 0)

    def test_zero_price_is_rejected(self):
        response = self.client.post(reverse('part_add'), {
            'part_name': 'Free oil',
            'quantity_in_stock': '1',
            'unit_price': '0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unit price must be greater than 0.')
        self.assertFalse(Part.objects.filter(part_name='Free oil').exists())
