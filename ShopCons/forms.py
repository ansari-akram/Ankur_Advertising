from django import forms
from django.contrib.auth.models import User
from . import models


# For Shopkeeper related form
class ShopkeeperUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class ShopkeeperForm(forms.ModelForm):
    class Meta:
        model = models.Shopkeeper
        fields = ['shopaddr', 'mobilenum', 'adhaarnum', 'gstnum', 'status', 'profile_pic', 'shpadhaar_pic',
                  'shoptype', 'shopname']


# For Consumer related form
class ConsumerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class ConsumerForm(forms.ModelForm):
    assignedShopId = forms.ModelChoiceField(queryset=models.Shopkeeper.objects.all().filter(status=True),
                                            empty_label="Name and Shop", to_field_name="shopname")

    class Meta:
        model = models.Consumer
        fields = ['address', 'mobilenum', 'adhaarnum', 'status', 'profile_pic', 'conadhaar_pic']


class AdmitForm(forms.ModelForm):
    shopId = forms.ModelChoiceField(queryset=models.Shopkeeper.objects.all().filter(status=True),
                                    empty_label="Shop Name and Department", to_field_name="user_id")
    consId = forms.ModelChoiceField(queryset=models.Consumer.objects.all().filter(status=True),
                                    empty_label="Consumer Name", to_field_name="user_id")

    class Meta:
        model = models.Admit
        fields = ['status']


class ConAdmitForm(forms.ModelForm):
    shopId = forms.ModelChoiceField(queryset=models.Shopkeeper.objects.all().filter(status=True),
                                    empty_label="Shop Name and Department", to_field_name="user_id")

    class Meta:
        model = models.Admit
        fields = ['status']


# For Contact Us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=100)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
