from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'product', 'rating', 'comment']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'input-rev', 'placeholder': 'e.g. Rahul'}),
            'rating': forms.Select(choices=[
                (5, '⭐⭐⭐⭐⭐ (5/5)'),
                (4, '⭐⭐⭐⭐ (4/5)'),
                (3, '⭐⭐⭐ (3/5)'),
                (2, '⭐⭐ (2/5)'),
                (1, '⭐ (1/5)'),
            ], attrs={'class': 'select-rev'}),
            'comment': forms.Textarea(attrs={'class': 'textarea-rev', 'rows': 5, 'placeholder': 'Share your experience with the product...'}),
        }
