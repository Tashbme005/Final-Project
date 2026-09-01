from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def paymentPage(request):
    data = {
        "title": "Payment page",
        "payment_options": ["Card", "Cash"]
    }
    return render(request, "payments/payments.html", data)

@login_required
def create_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')

        new_payment = Payment(
            payment_method=payment_method,
            amount=amount
        )
        new_payment.save()
        return redirect('paymentPage')
    return render(request, 'payments/payment_form.html')

@login_required
def create_receipt(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        receipt_number = request.POST.get('receipt_number')

        new_receipt = Receipt(
            payment_id=payment_id,
            receipt_number=receipt_number
        )
        new_receipt.save()
        return redirect('paymentPage')
    return render(request, 'payments/receipt_form.html')

@login_required
def receipt_details(request, receipt_id):
    receipt = Receipt.objects.get(pk=receipt_id)
    return render(request, 'payments/view_receipt.html', {'receipt': receipt})

@login_required
def payment_details(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    return render(request, 'payments/view_payment.html', {'payment': payment})  

@login_required
def update_payment(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')

        payment.payment_method = payment_method
        payment.amount = amount
        payment.save()
        return redirect('paymentPage')
    return render(request, 'payments/payment_form.html', {'payment': payment})

@login_required
def update_receipt(request, receipt_id):
    receipt = Receipt.objects.get(pk=receipt_id)
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        receipt_number = request.POST.get('receipt_number')

        receipt.payment_id = payment_id
        receipt.receipt_number = receipt_number
        receipt.save()
        return redirect('paymentPage')
    return render(request, 'payments/receipt_form.html', {'receipt': receipt})


@login_required
def delete_payment(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    payment.delete()
    return redirect('paymentPage')  

@login_required
def delete_receipt(request, receipt_id):
    receipt = Receipt.objects.get(pk=receipt_id)
    receipt.delete()
    return redirect('paymentPage')

@login_required
def payment_history(request):
    payments = Payment.objects.all()
    return render(request, 'payments/payment_history.html', {'payments': payments})

def total_payment_amount(request):
    total = Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']
    return total