from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from employees.access import role_required, ADMIN, SENIOR, TECHNICIAN, user_role
from orders.models import Order
from .models import Payment, Receipt
from .forms import PaymentForm


@role_required(ADMIN, SENIOR, TECHNICIAN)
def payment_list(request):
    payments = Payment.objects.select_related('order', 'order__vehicle', 'order__vehicle__customer').order_by('-paid_at')
    employee = getattr(request.user, 'employee', None)
    if user_role(request.user) == TECHNICIAN and employee:
        payments = payments.filter(order__technicians=employee)
    total = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    return render(request, 'payments.html', {'payments': payments, 'total': total})


@role_required(ADMIN)
def payment_add(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            Receipt.objects.create(
                payment=payment,
                receipt_number=f'OAS-{payment.payment_id:04d}',
            )
            payment.order.status = 'Completed'
            payment.order.save()
            messages.success(request, 'Payment recorded.')
            return redirect('receipt_view', payment_id=payment.payment_id)
    else:
        initial = {}
        order_id = request.GET.get('order')
        if order_id:
            initial['order'] = order_id
            order = Order.objects.filter(pk=order_id).first()
            if order:
                initial['amount_paid'] = order.service_total()
        form = PaymentForm(initial=initial)
    return render(request, 'payment_form.html', {
        'form': form,
        'title': 'Record Payment',
        'note': 'Labour is UGX 20,000. Wheel alignment is UGX 30,000 and wheel balance is UGX 20,000.',
    })


@role_required(ADMIN, SENIOR, TECHNICIAN)
def receipt_view(request, payment_id):
    payments = Payment.objects.select_related('order', 'order__vehicle', 'order__vehicle__customer')
    employee = getattr(request.user, 'employee', None)
    if user_role(request.user) == TECHNICIAN and employee:
        payments = payments.filter(order__technicians=employee)
    payment = get_object_or_404(payments, pk=payment_id)
    receipt = payment.receipt_set.first()
    services = payment.order.service.all()
    return render(request, 'receipt.html', {
        'payment': payment,
        'receipt': receipt,
        'services': services,
    })
