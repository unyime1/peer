from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.forms import ModelForm
from users.models import *


STATUS = (
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'), 
)

class MergeForm(ModelForm):
    status = forms.ChoiceField(choices=STATUS, required=False)

    class Meta:
        model = Merge
        fields = ['status']


class MinimumPHForm(ModelForm):
    amount = forms.CharField(max_length=180, required=False, label='Amount', widget=forms.TextInput(attrs={'type':'number', 'placeholder': 'Please Input an Amount without comma.'}))

    class Meta:
        model = MinimumPH
        fields = ['amount']


class MaxPHForm(ModelForm):
    amount = forms.CharField(max_length=180, required=False, label='Amount', widget=forms.TextInput(attrs={'type':'number', 'placeholder': 'Please Input an Amount without comma.'}))

    class Meta:
        model = MaxPH
        fields = ['amount']


class PercentageReturnForm(ModelForm):
    amount = forms.CharField(max_length=180, required=False, label='Amount', widget=forms.TextInput(attrs={'type':'number', 'placeholder': 'Please include a value'}))

    class Meta:
        model = PercentageReturn
        fields = ['amount']

"""
class DownPaymentForm(ModelForm):
    amount = forms.CharField(max_length=180, required=False, label='Amount', widget=forms.TextInput(attrs={'placeholder': 'Please include a value'}))

    class Meta:
        model = DownPaymentPercentage
        fields = ['amount']
"""


class DaysToGHForm(ModelForm):
    amount = forms.CharField(max_length=180, required=False, label='Amount', widget=forms.TextInput(attrs={'type':'number', 'placeholder': 'Please include a value'}))

    class Meta:
        model = DaystoGH
        fields = ['amount']


class ReferralBonusForm(ModelForm):
    amount = forms.CharField(max_length=180, required=False, label='Amount', widget=forms.TextInput(attrs={'type':'number', 'placeholder': 'Please include a value'}))

    class Meta:
        model = ReferralBonus
        fields = ['amount']


class MergeCustomersForm(forms.Form):
    provider = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    receiver = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.CharField(max_length=180, label='Amount', widget=forms.TextInput(attrs={'type':'number', 'placeholder': 'Please Input an Amount'}))
    transaction_id = forms.CharField(max_length=180, required=True, label='Transaction ID', widget=forms.TextInput(attrs={'placeholder': 'Please Input Your Transaction ID'}))

    def clean_transaction_id(self):
        """this function handles phonenumber cleaning"""
        transaction_id = self.cleaned_data['transaction_id']
        match = HelpTable.objects.filter(transaction_id=transaction_id).exists()
        
        if match:
            return transaction_id
        else:
            raise forms.ValidationError(_('This transaction ID does not exist! Please check the help request and note the correct transaction ID!'))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].choices= [(customer.username, customer.username) for customer in Customer.objects.all()]
        self.fields['receiver'].choices= [(customer.username, customer.username) for customer in Customer.objects.all()]

    
class AdminAccountSettingForm(ModelForm):
    bank_name = forms.CharField(max_length=180, required=False, label='Bank Name', widget=forms.TextInput(attrs={'placeholder': 'Please include a value'}))
    account_name = forms.CharField(max_length=180, required=False, label='Account Name', widget=forms.TextInput(attrs={'placeholder': 'Please include a value'}))
    account_number = forms.CharField(max_length=180, required=False, label='Account Number', widget=forms.TextInput(attrs={'placeholder': 'Please include a value'}))
    account_type = forms.CharField(max_length=180, required=False, label='Account Type', widget=forms.TextInput(attrs={'placeholder': 'Please include a value'}))
    
    class Meta:
        model = AdminAccountSetting
        fields = ['bank_name', 'account_name', 'account_number', 'account_type']


class ActivationFeeSettingForm(ModelForm):
    STATUS = (
        ('Admin', 'Admin'),
        ('Referrer', 'Referrer'), 
    )
    option = forms.ChoiceField(choices=STATUS, required=False)

    class Meta:
        model = ActivationFeeSetting
        fields = ['option']
    