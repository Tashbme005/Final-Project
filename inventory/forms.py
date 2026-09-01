from decimal import Decimal
from django import forms
from oas.validators import clean_text
from .models import Part, PartsRequest


class PartForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Part
        fields = ['part_name', 'quantity_in_stock', 'unit_price']
        error_messages = {
            'part_name': {'required': 'Enter the part name.'},
            'quantity_in_stock': {'required': 'Enter the quantity in stock.', 'invalid': 'Enter a whole number.'},
            'unit_price': {'required': 'Enter the unit price in UGX.', 'invalid': 'Enter a valid amount.'},
        }
        widgets = {
            'part_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1'}),
        }

    def clean_part_name(self):
        return clean_text(self.cleaned_data.get('part_name'), 'Part name', min_length=2, max_length=100)

    def clean_unit_price(self):
        price = self.cleaned_data.get('unit_price')
        if price is None or price <= Decimal('0'):
            raise forms.ValidationError('Unit price must be greater than 0.')
        return price


class PartsRequestForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = PartsRequest
        fields = ['part', 'quantity', 'comment', 'requested_by', 'issued_to']
        labels = {
            'issued_to': 'Issue to technician',
        }
        error_messages = {
            'part': {'required': 'Select a part.'},
            'quantity': {'required': 'Enter the quantity needed.'},
            'requested_by': {'required': 'Select who is requesting the part.'},
        }
        widgets = {
            'part': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'requested_by': forms.Select(attrs={'class': 'form-select'}),
            'issued_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        return quantity
