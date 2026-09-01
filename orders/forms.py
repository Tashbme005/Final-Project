from django import forms
from .models import Customer, Vehicle, Inspection

class MyForm(forms.Form):
    template_name = "form_snippet.html"

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

        labels = {
            "customer_name": "Full Name",
            "customer_email": "Email",
            "phone_number": "Phone Number"
        }

        error_messages = {
            "customer_name": {
                "required": "Provide Full names"
            },
            "customer_email": {
                "required": "Provide the customer's preferd email"
            },
            "phone_number": {
                "required": "Provide customer's active phone number"
            }
        }

    def clean_customer_name(self):
        customer_name = self.cleaned_data["customer_name"]

        if len(customer_name) >=2:
            raise forms.ValidationError("Provide customers full name")
        
        return customer_name


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"

        labels = {
            "size": "Car Size",
            "car_model": "Car Model",
            "number_plate": "Car Number Plate"
        }

        error_messages = {
            "size": {
                "required": "Use the car sizes provided in the drop down options"
            },
            "car_model": {
                "required": "Provide car model"
            },
            "number_plate": {
                "required": "Provide the car number plate"
            }
        }

    def clean_number_plate(self):
        number_plate = self.cleaned_data["number_plate"]

        if len(number_plate) < 5:
            raise forms.ValidationError("Provide a valid number plate")

        return number_plate

class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = "__all__"
        widgets = {
            "done_at": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }

        labels = {
            "findings": "Findings",
            "recommended_service": "Recommended Service",
            "done_at": "Time of Inspection"
        }

        error_messages = {
            "findings": {
                "required": "Give a short report on what issues the car had"
            },
            "recommended_service": {
                "required": "Write down the recommende service to be done"
            },
            "done_at": {
                "required": "Provide time of inspection"
            }
        }

    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

        labels = {
            "description": "Order Description"
        }

        error_messages = {
            "description": {
                "required": "Provide a short description of the order"
            }
        }

