from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'category',
            'price',
            'condition',
            'image',
            'availability_status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
