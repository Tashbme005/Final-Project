from django import forms
from .models import Part

class MyForm(forms.Form):
    template_name = "form_snippet.html"


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = "__all__"

        labels = {
            "part_name": "Part Name",
            "quantity_in_stock": "Available Stock",
            "unit_price": "Unit Price"
        }

        error = {
            "part_name": {
                "required": "Use the drop down options provided"
            },
            "quatity_in_stock": {
                "required": "Available in stock"
            },
            "unit_price": {
                "required": "Prices are based on size"
            },
        }

    def clean_quantity_in_stock(self):
        quantity_in_stock = self.cleaned_data["quantity_in_stock"]

        if len(quantity_in_stock) < 5:
            raise forms.ValidationError("Limited stock")

        return quantity_in_stock


class PartsRequestForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = "__all__"

        labels = {
            "part_request": "Part Request",
            "quantity": "Quantity",
            "comment": "Comment"
        }

        error = {
            "part_request": {
                "required": "Use the drop down options provided"
            },
            "quantity": {
                "required": "Available in stock"
            },
            "comment": {
                "required": "Prices are based on size"
            },
        }

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if len(quantity) < 5:
            raise forms.ValidationError("Limited stock")

        return quantity

    