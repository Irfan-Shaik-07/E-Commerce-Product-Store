from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.RadioSelect(choices=[
                ('Credit/Debit Card', 'Credit / Debit Card'),
                ('UPI', 'UPI (Google Pay, PhonePe, Paytm)'),
                ('Net Banking', 'Net Banking'),
            ])
        }
