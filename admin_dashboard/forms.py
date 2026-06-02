from django import forms
from homepage.models import Product
from .models import AdminActivityLog

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'rating', 'image_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. iPhone 16 Pro'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'e.g. 139999.00'}),
            'description': forms.Textarea(attrs={'class': 'form-input form-textarea', 'rows': 4, 'placeholder': 'Enter product details...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': '1.0', 'max': '5.0', 'placeholder': 'e.g. 4.8'}),
            'image_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'e.g. https://images.unsplash.com/...'}),
        }

class AdminActivityLogForm(forms.ModelForm):
    class Meta:
        model = AdminActivityLog
        fields = ['action_type', 'action_details']
        widgets = {
            'action_type': forms.Select(attrs={'class': 'form-select'}),
            'action_details': forms.Textarea(attrs={'class': 'form-input form-textarea', 'rows': 3, 'placeholder': 'Details about the action...'}),
        }
