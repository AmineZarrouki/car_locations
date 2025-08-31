from django import forms
from .models import User, Car, Admin, Rental

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number", "address", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["make", "model", "year", "color", "license_plate", "daily_rate", "availability_status"]

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["user", "permissions"]

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ["user", "car", "start_date", "end_date", "total_cost", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


