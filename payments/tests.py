from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from employees.models import Employee
from employees.test_helpers import login_as_admin
from orders.models import Customer, Vehicle, Order
from services.models import Service
from .models import Payment, Receipt


class PaymentTests(TestCase):
    def setUp(self):
        login_as_admin(self.client)
        customer = Customer.objects.create(
            customer_name='David Otim',
            customer_email='david.otim@email.com',
            phone_number='0704005566',
        )
        vehicle = Vehicle.objects.create(
            customer=customer,
            size='Heavy',
            car_model='Isuzu FVR',
            number_plate='UAE 789C',
        )
        technician = Employee.objects.create(
            employee_name='James Oyera',
            date_of_birth=date(1984, 3, 12),
            phone_number='0772123456',
            email='james.oyera@oasbay.ug',
            nin='CM840312001ABC',
        )
        labour = Service.objects.create(
            service_name='Labour charge',
            description='Standard bay labour',
            unit_cost=Decimal('20000'),
        )
        self.order = Order.objects.create(
            vehicle=vehicle,
            description='Labour after owner bought oil and filter',
            status='In Progress',
        )
        self.order.service.add(labour)
        self.order.technicians.add(technician)

    def test_payment_creates_a_receipt_and_completes_the_job(self):
        payment = Payment.objects.create(
            order=self.order,
            payment_method='Cash',
            amount_paid=self.order.service_total(),
        )
        receipt = Receipt.objects.create(
            payment=payment,
            receipt_number='OAS-0001',
        )
        self.assertEqual(payment.amount_paid, Decimal('20000'))
        self.assertEqual(str(receipt), 'OAS-0001')
        self.assertEqual(str(payment), 'Payment 1 - Paid')

    def test_payment_pages_open(self):
        payment = Payment.objects.create(
            order=self.order,
            payment_method='Cash',
            amount_paid=Decimal('20000'),
        )
        Receipt.objects.create(payment=payment, receipt_number='OAS-0001')
        self.assertEqual(self.client.get(reverse('payment_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('payment_add')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('receipt_view', args=[payment.payment_id])).status_code,
            200,
        )

    def test_recording_payment_issues_a_receipt(self):
        response = self.client.post(reverse('payment_add'), {
            'order': self.order.order_id,
            'payment_method': 'Cash',
            'amount_paid': '20000',
            'comment': 'Owner already bought parts',
        })
        self.assertEqual(response.status_code, 302)
        payment = Payment.objects.get(order=self.order)
        self.assertTrue(Receipt.objects.filter(payment=payment).exists())
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Completed')
        self.assertEqual(payment.receipt_set.first().receipt_number, f'OAS-{payment.payment_id:04d}')

    def test_empty_payment_form_shows_error_messages(self):
        response = self.client.post(reverse('payment_add'), {
            'order': '',
            'payment_method': '',
            'amount_paid': '',
            'comment': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select the job card being paid.')
        self.assertEqual(Payment.objects.count(), 0)
