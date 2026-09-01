from decimal import Decimal
from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Payment
        fields = ['order', 'payment_method', 'amount_paid', 'comment']
        error_messages = {
            'order': {'required': 'Select the job card being paid.'},
            'payment_method': {'required': 'Select Cash or Card.'},
            'amount_paid': {'required': 'Enter the amount paid in UGX.', 'invalid': 'Enter a valid amount.'},
        }
        widgets = {
            'order': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_amount_paid(self):
        amount = self.cleaned_data.get('amount_paid')
        if amount is None or amount <= Decimal('0'):
            raise forms.ValidationError('Amount paid must be greater than 0.')
        return amount

    def clean_comment(self):
        return (self.cleaned_data.get('comment') or '').strip()
