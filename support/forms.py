from django import forms
from .models import SupportTicket

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-sup', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'input-sup', 'placeholder': 'Enter your email'}),
            'subject': forms.TextInput(attrs={'class': 'input-sup', 'placeholder': 'How can we help you?'}),
            'message': forms.Textarea(attrs={'class': 'textarea-sup', 'rows': 6, 'placeholder': 'Describe your issue or question in detail...'}),
        }
