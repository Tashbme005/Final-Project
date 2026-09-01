from django import forms
from oas.validators import clean_email_address, clean_full_name, clean_nin, clean_text, clean_ug_phone
from .models import Employee, Role


class EmployeeForm(forms.ModelForm):
    use_required_attribute = False

    id_kind = forms.ChoiceField(
        label='Do you have a NIN?',
        choices=[
            ('yes', 'Yes, I have a NIN (Ugandan)'),
            ('no', "No, I don't have a NIN (foreigner)"),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='yes',
        error_messages={'required': 'Select whether this person has a NIN.'},
    )

    class Meta:
        model = Employee
        fields = ['employee_name', 'date_of_birth', 'phone_number', 'email', 'job_role', 'nin', 'passport_number']
        error_messages = {
            'employee_name': {'required': 'Enter the staff member full name.'},
            'date_of_birth': {'required': 'Enter the date of birth.'},
            'phone_number': {'required': 'Enter a phone number.'},
            'email': {'required': 'Enter an email address.', 'invalid': 'Enter a valid email address.'},
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_date_of_birth'}),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name and last name',
                'autocomplete': 'name',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0772123456',
                'maxlength': '10',
                'inputmode': 'numeric',
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'job_role': forms.Select(attrs={'class': 'form-select'}),
            'nin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'for example CM840312001ABC',
                'maxlength': '20',
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Passport number',
                'maxlength': '20',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['id_kind'].initial = 'yes' if self.instance.has_nin else 'no'
        self.order_fields([
            'employee_name',
            'date_of_birth',
            'phone_number',
            'email',
            'job_role',
            'id_kind',
            'nin',
            'passport_number',
        ])

    def clean_employee_name(self):
        return clean_full_name(self.cleaned_data.get('employee_name'), 'Staff name')

    def clean_phone_number(self):
        return clean_ug_phone(self.cleaned_data.get('phone_number'))

    def clean_email(self):
        return clean_email_address(self.cleaned_data.get('email'))

    def clean_nin(self):
        if self.data.get('id_kind') == 'no':
            return ''
        return clean_nin(self.cleaned_data.get('nin'))

    def clean_passport_number(self):
        if self.data.get('id_kind') != 'no':
            return ''
        return clean_text(self.cleaned_data.get('passport_number'), 'Passport number', min_length=6, max_length=50)

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.has_nin = self.cleaned_data.get('id_kind') == 'yes'
        if employee.has_nin:
            employee.passport_number = ''
        else:
            employee.nin = ''
        if commit:
            employee.save()
        return employee


class RoleForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Role
        fields = ['employee', 'role', 'description']
        labels = {
            'employee': 'Staff member',
            'role': 'Job role title',
            'description': 'What they do',
        }
        help_texts = {
            'role': 'For example Alignment specialist, Stores clerk, or Cashier.',
            'description': 'Optional short note about this role at the bay.',
        }
        error_messages = {
            'employee': {'required': 'Select the staff member for this job role.'},
            'role': {'required': 'Enter the job role title.'},
        }
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alignment specialist'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_role(self):
        return clean_text(self.cleaned_data.get('role'), 'Job role', min_length=3, max_length=40)

    def clean_description(self):
        return (self.cleaned_data.get('description') or '').strip()

