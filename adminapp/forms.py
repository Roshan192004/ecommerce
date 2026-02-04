from django import forms
from .models import Category, HealthCategory, DeliveryLocation,Medicine

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

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'price', 'image', 'stock', 'category']