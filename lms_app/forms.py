from django import forms
from .models import *

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            'product_name',
            'real_quantity',
            'inventory_quantity',
            'image'
        ]
        widgets = {
            'product_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Parent Code'}),
            'real_quantity' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Enter Parent Code', 'readonly': True}),
            'inventory_quantity' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Enter Real Quantity'}),
            'image' : forms.FileInput(attrs={'class': 'form-control', 'style':'height:60px'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_id',
            'product_name',
            'category',
            'amount_of_parties',
            'image',
            'pack_name'
        ]
        widgets = {
            'image' : forms.FileInput(attrs={'class': 'form-control', 'style':'height:60px'}),
            'product_id' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Name'}),
            'product_name' : forms.Select(attrs={'class': 'form-control', 'placeholder':'Enter Parent Code'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
            'amount_of_parties' : forms.HiddenInput(attrs={'class': 'form-control', 'readonly': True}),
            'pack_name' : forms.Select(attrs={'class': 'form-control'})
        }


class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = [
            # 'party_code',
            'party_name',
            'leader_name',
            'wh_leader',
            'start_date',
            # 'end_date',
        ]
        widgets = {
            # 'party_code' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Enter Code of Party', 'readonly':True}),
            'party_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Name of Party'}),
            'leader_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Name of Leader'}),
            'wh_leader' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Name of WareHouse Leader'}),
            'start_date' : forms.DateInput(attrs={'class': 'form-control', 'placeholder':'Enter Start Date of Party', 'type':'date'}),
            # 'end_date' : forms.DateInput(attrs={'class': 'form-control', 'placeholder':'Enter Code of Party', 'readonly':True, 'type':'date'}),
        }

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically fetch products from the Product table
        product_choices = [('', 'Select a product')]
        self.fields['product_id'].widget = forms.Select(attrs={'class': 'form-control'})
        
    class Meta:
        model = Order
        fields = [
            'party_code',
            'product_id',
            'state',
        ]
        widgets = {
            'party_code' : forms.TextInput(attrs={'class': 'form-control', 'readonly':True}),
            'state' : forms.HiddenInput(),
        }

class MaintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically fetch products from the Product table
        product_choices = [('', 'Select a product')]
        self.fields['product_id'].widget = forms.Select(attrs={'class': 'form-control'})
        
    class Meta:
        model = Maintenance
        fields = [
            'product_id',
        ]
        
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            'pack_name',
        ]
        widgets = {
            'pack_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter the Name of Package'}),
        }