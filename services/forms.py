from decimal import Decimal
from django import forms
from oas.validators import clean_text
from .models import Service


class ServiceForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Service
        fields = ['service_name', 'description', 'unit_cost']
        error_messages = {
            'service_name': {'required': 'Enter the service name.'},
            'description': {'required': 'Enter a short description.'},
            'unit_cost': {'required': 'Enter the charge in UGX.', 'invalid': 'Enter a valid amount.'},
        }
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def clean_service_name(self):
        return clean_text(self.cleaned_data.get('service_name'), 'Service name', min_length=3, max_length=50)

    def clean_description(self):
        return clean_text(self.cleaned_data.get('description'), 'Description', min_length=5, max_length=500)

    def clean_unit_cost(self):
        cost = self.cleaned_data.get('unit_cost')
        if cost is None or cost < Decimal('0'):
            raise forms.ValidationError('Unit cost cannot be negative.')
        return cost
