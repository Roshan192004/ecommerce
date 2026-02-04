from django import forms
from .models import Category, HealthCategory, DeliveryLocation

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']



class HealthCategoryForm(forms.ModelForm):
    class Meta:
        model = HealthCategory
        fields = ['name', 'image', 'is_active']


class DeliveryLocationForm(forms.ModelForm):
    class Meta:
        model = DeliveryLocation
        fields = ['city', 'pincode']

