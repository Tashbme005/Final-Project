from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from employees.test_helpers import login_as_admin
from .models import Service


class ServiceTests(TestCase):
    def setUp(self):
        login_as_admin(self.client)
    def test_labour_alignment_and_balance_charges(self):
        labour = Service.objects.create(
            service_name='Labour charge',
            description='Charged after the owner buys parts',
            unit_cost=Decimal('20000'),
        )
        alignment = Service.objects.create(
            service_name='Wheel alignment',
            description='Wheel alignment for one car',
            unit_cost=Decimal('30000'),
        )
        balance = Service.objects.create(
            service_name='Wheel balance',
            description='Wheel balance for one car',
            unit_cost=Decimal('20000'),
        )

        self.assertEqual(labour.unit_cost, Decimal('20000'))
        self.assertEqual(alignment.unit_cost, Decimal('30000'))
        self.assertEqual(balance.unit_cost, Decimal('20000'))
        self.assertEqual(str(labour), 'Labour charge')

    def test_service_pages_open(self):
        self.assertEqual(self.client.get(reverse('service_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('service_add')).status_code, 200)

    def test_service_can_be_added_from_the_form(self):
        response = self.client.post(reverse('service_add'), {
            'service_name': 'Greasing',
            'description': 'Minor greasing service',
            'unit_cost': '20000',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Service.objects.filter(service_name='Greasing').exists())

    def test_empty_service_form_shows_error_messages(self):
        response = self.client.post(reverse('service_add'), {
            'service_name': '',
            'description': '',
            'unit_cost': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter the service name.')
        self.assertEqual(Service.objects.count(), 0)
