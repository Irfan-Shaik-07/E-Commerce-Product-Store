from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'city', 'zip_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-chk', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'input-chk', 'placeholder': 'johndoe@example.com'}),
            'address': forms.TextInput(attrs={'class': 'input-chk', 'placeholder': '123 Main Street'}),
            'city': forms.TextInput(attrs={'class': 'input-chk', 'placeholder': 'New Delhi'}),
            'zip_code': forms.TextInput(attrs={'class': 'input-chk', 'placeholder': '110001'}),
        }
