from django import forms
from .models import Employee, Role

class MyForm(forms.Form):
    template_name = "form_snippet.html"

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"})
        }

        labels = {
            "employee_name": "Name",
            "date_of_birth": "DOB",
            "phone_number": "Phone Number",
            "email": "Email",
            "nin": "NIN",
            "passport_number": "Passport Number"
        }

    error_messages = {
        "name": {
            "required": "Full official name required"
        },
        "date_of_birth": {
            "required": "Provide your date of birth as written on your birth certificate"
        },
        "phone_number": {
            "required": "Provide currently available number"
        },
        "email": {
            "required": "Provide email in your official names"
        },
        "nin": {
            "required": "Provide your national identification number"
        },
        "passport": {
            "required": "Provide your passport number in case your not Ugandan"
        }
    }

    def clean_employee_name(self):
        employee_name = self.cleaned_data["employee_name"].strip()

        if len(employee_name.split()) < 2:
            raise forms.ValidationError("Enter your first name, last name and any additional names")

        return employee_name

    def clean_email(self):
        email = self.cleaned_data["email"].lower() #lower ignores capital letters
        employee_name = self.cleaned_data["employee_name"].lower()

        name = employee_name.split()#splits separate the employee name into separate names
        email_name = email.split("@")[0].replace("."," ").replace("-", " ").replace("_", " ")#split(@)[0] picks out whats before the @, replace()handles names with the stated puntuation signs in them
        email_names = email_name.split()

        if len(set(name) & set(email_names)) < 2:
            raise forms.ValidationError("Provide email with at least two of your stated names")

        return email

    
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"

        labels = {
            "employee": "Employee",
            "role": "Role",
            "description": "Description"
        }

        error_messages = {
            "employee": {
                "required": "Select employee from the list"
            },
            "role": {
                "required": "Provide role of the employee"
            },
            "description": {
                "required": "Provide a brief description of the role"
            }
        }

    def clean_role(self):
        role = self.cleaned_data["role"].strip()

        if len(role.split()) < 1:
            raise forms.ValidationError("Provide a valid role")

        return role

        