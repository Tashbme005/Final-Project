from django import forms
from oas.validators import clean_email_address, clean_full_name, clean_text, clean_ug_phone
from .models import Customer, Vehicle, Inspection, Order


class CustomerForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Customer
        fields = ['customer_name', 'customer_email', 'phone_number']
        error_messages = {
            'customer_name': {'required': 'Enter the customer full name.'},
            'customer_email': {'required': 'Enter the customer email.', 'invalid': 'Enter a valid email address.'},
            'phone_number': {'required': 'Enter the customer phone number.'},
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name and last name'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0772123456'}),
        }

    def clean_customer_name(self):
        return clean_full_name(self.cleaned_data.get('customer_name'), 'Customer name')

    def clean_customer_email(self):
        return clean_email_address(self.cleaned_data.get('customer_email'))

    def clean_phone_number(self):
        return clean_ug_phone(self.cleaned_data.get('phone_number'))


class VehicleForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Vehicle
        fields = ['customer', 'size', 'car_model', 'number_plate']
        error_messages = {
            'customer': {'required': 'Select the vehicle owner.'},
            'size': {'required': 'Select Heavy, Commercial or Small.'},
            'number_plate': {'required': 'Enter the number plate.'},
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'car_model': forms.TextInput(attrs={'class': 'form-control'}),
            'number_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UAA 123A'}),
        }

    def clean_car_model(self):
        return clean_text(self.cleaned_data.get('car_model'), 'Car model', min_length=2, max_length=50)

    def clean_number_plate(self):
        plate = clean_text(self.cleaned_data.get('number_plate'), 'Number plate', min_length=5, max_length=20)
        return plate.upper()


class InspectionForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Inspection
        fields = ['vehicle', 'findings', 'recommended_service']
        error_messages = {
            'vehicle': {'required': 'Select the vehicle that was inspected.'},
            'findings': {'required': 'Write a short report of the findings.'},
            'recommended_service': {'required': 'Write the recommended service.'},
        }
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'findings': forms.TextInput(attrs={'class': 'form-control'}),
            'recommended_service': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_findings(self):
        return clean_text(self.cleaned_data.get('findings'), 'Findings', min_length=5, max_length=200)

    def clean_recommended_service(self):
        return clean_text(self.cleaned_data.get('recommended_service'), 'Recommended service', min_length=3, max_length=100)


class OrderForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Order
        fields = ['vehicle', 'technicians', 'service', 'description', 'status']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'technicians': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
            'service': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'service': 'Services needed',
            'technicians': 'Technician(s) assigned',
        }
        help_texts = {
            'technicians': 'Hold Ctrl to select more than one technician.',
            'service': 'Hold Ctrl to select more than one service.',
        }
        error_messages = {
            'vehicle': {'required': 'Select the vehicle for this job card.'},
        }

    def clean_description(self):
        value = (self.cleaned_data.get('description') or '').strip()
        return value

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('service'):
            self.add_error('service', 'Select at least one service.')
        if not cleaned.get('technicians'):
            self.add_error('technicians', 'Assign at least one technician.')
        return cleaned
