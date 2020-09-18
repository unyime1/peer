"""this module holds the users app forms"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import *
from mains.models import *


STATES = (
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'), 
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
    ('FCT', 'FCT'),
    ('Sokoto', 'Sokoto'),
    
)

TYPE = (
    ('Savings', 'Savings'),
    ('Current', 'Current'),
)
 

class RegistrationForm(UserCreationForm): 
    """this class handles the user registration form"""
    first_name = forms.CharField(max_length=30, required=True, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=30, required=True, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'})) 
    email = forms.EmailField(max_length=254, required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))


    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2'] #allowed fields

    def clean_email(self):
        """this function handles email cleaning"""
        email = self.cleaned_data['email']
        match = User.objects.filter(email=email).exists()
        
        if match:
            raise forms.ValidationError(_('The email already exists. Choose another'))
        else:
            return email


class AddressForm(forms.Form): 
    """this class handles the user registration form 2"""
    #address = forms.CharField(max_length=100, required=True, label='Address', widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    #city = forms.CharField(max_length=100, required=True, label='City', widget=forms.TextInput(attrs={'placeholder': 'City'}))
    #state = forms.ChoiceField(choices=STATES)
    phone_number = forms.CharField(max_length=40, required=True, label='Phone Number', widget=forms.TextInput(attrs={'type':'number','placeholder': 'Phone Number'}))
    sponsor = forms.CharField(max_length=40, required=False, label='Sponsor', widget=forms.TextInput(attrs={'placeholder': "Referrer's/Sponsor's Username(Optional)"}))

    def clean_phone_number(self):
        """this function handles phonenumber cleaning"""
        phone_number = self.cleaned_data['phone_number']
        match = Customer.objects.filter(phone_number=phone_number).exists()
        
        if match:
            raise forms.ValidationError(_('The phone number already exists. Choose another'))
        else:
            return phone_number

    def clean_sponsor(self):  
        """sponsor cleaning"""
        sponsor = self.cleaned_data['sponsor']
        
        if not self.data['sponsor']:
            return sponsor

        match = Customer.objects.filter(username=sponsor).exists()
        
        if match:
            return sponsor   
        else:
            raise forms.ValidationError(_('We do not have this user on our system. Please confirm your entry'))
    
           


class LoginForm(forms.Form):
    """this class defines the login form"""
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    

class BankingForm(ModelForm):
    """this class handles the user registration form 3"""
    bank_name = forms.CharField(max_length=100, required=True, label='Bank Name', widget=forms.TextInput(attrs={'placeholder': 'Bank Name'}))
    account_name = forms.CharField(max_length=100, required=True, label='Account Name', widget=forms.TextInput(attrs={'placeholder': 'Account Name'}))
    account_number = forms.CharField(max_length=100, required=True, label='Account Number', widget=forms.TextInput(attrs={'type':'number','placeholder': 'Account Number'}))
    account_type = forms.ChoiceField(choices=TYPE)
    
    class Meta:
        model = Banking
        fields = ['bank_name', 'account_name', 'account_number', 'account_type']



class SupportForm(ModelForm):
    """this class defines the support form"""
    message = forms.CharField(max_length=1000, required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Message'}))
    class Meta:
        model = Contact
        fields = ['message']


class ProvideHelpForm(forms.Form):
    """this class handles the PH form"""
    amount = forms.CharField(max_length=180, required=True, label='Amount', widget=forms.TextInput(attrs={'type':'number','placeholder': 'How much do you want to invest?'}))
    
    def clean_amount(self):
        """this function handles amount cleaning"""
        amount = self.cleaned_data['amount']
        latest_min_ph_setting = MinimumPH.objects.all().order_by('-date').first()
        latest_max_ph_setting = MaxPH.objects.all().order_by('-date').first()

        if int(amount) < int(latest_min_ph_setting.amount):
            raise forms.ValidationError(_('Your amount is too low. Enter larger one.'))
        if int(amount) > int(latest_max_ph_setting.amount):
            raise forms.ValidationError(_('Your amount is too high. Enter a smaller one.'))
        else:
            return amount


class GetHelpForm(forms.Form):
    """this class handles the GH form"""
    amount = forms.CharField(max_length=180, required=True, label='Amount', widget=forms.TextInput(attrs={'type':'number','placeholder': 'How much help do you want?'}))

    def clean_amount(self):
        """this function handles email cleaning"""
        amount = self.cleaned_data['amount']
        
        if int(amount) < 100:
            raise forms.ValidationError(_('Your amount is too low. Choose another.'))
        else:
            return amount




class ProofOfPaymentForm(forms.Form):
    """this class handles the proof of payment submission form"""
    transaction_id = forms.CharField(max_length=180, required=True, label='Transaction ID', widget=forms.TextInput(attrs={'placeholder': 'Please Input Your Transaction ID'}))
    image = forms.ImageField()

    def clean_transaction_id(self):
        """this function handles phonenumber cleaning"""
        transaction_id = self.cleaned_data['transaction_id']
        match = HelpTable.objects.filter(transaction_id=transaction_id).exists()
        
        if match:
            return transaction_id
        else:
            raise forms.ValidationError(_('This transaction ID does not exist! Please check and try again.'))
      

"""
#removed per client request
class AdminProofOfPaymentForm(forms.Form):
   
    transaction_id = forms.CharField(max_length=180, required=True, label='Transaction ID', widget=forms.TextInput(attrs={'placeholder': 'Please Input Your Transaction ID'}))
    image = forms.ImageField()

    def clean_transaction_id(self):
       
        transaction_id = self.cleaned_data['transaction_id']
        match = HelpTable.objects.filter(transaction_id=transaction_id).exists()
        
        if match:
            return transaction_id
        else:
            raise forms.ValidationError(_('This transaction ID does not exist! Please check and try again.'))
"""

class ActivationProofForm(forms.Form):
    """this class defines the proof of activation fee payment form"""
    image = forms.ImageField()