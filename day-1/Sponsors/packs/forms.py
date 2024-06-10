from django import forms
from .models import Subscription, Item

class SubscriptionForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('TPE','Très Petite Entreprise'),
        ('PMI','Petite et Moyenne Industrie'),
        ('PME','Petite et Moyenne Entreprise'),
        ('SU','StartUp'),
        ('autres','Autres'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    company_type = forms.ChoiceField(choices=COMPANY_TYPE_CHOICES, widget=forms.Select)

    class Meta:
        model = Subscription
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'address', 'gender', 'company_name', 'company_type', 
            'creation_date', 'items'  # Add items field here
        ]
        widgets = {
            'items': forms.CheckboxSelectMultiple,
        }

class ItemSelectionForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.CheckboxSelectMultiple)
