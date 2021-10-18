from django import forms
from .models import Product, Category, User

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [            
            "category",
            "title",
            "start_bid",
            "description",
            "image"
        ]
        widgets = {
            "category": forms.Select(choices=Category.objects.all()),
            
            
            
        }