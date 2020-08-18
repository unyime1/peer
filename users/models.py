from django.db import models
from django.contrib.auth.models import User


"""
class Address(models.Model):
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)

    def __str__(self): 
        return str(self.customer.username)
"""


class Banking(models.Model):
    bank_name = models.CharField(max_length=200, null=True)
    account_name = models.CharField(max_length=200, null=True)
    account_number = models.CharField(max_length=200, null=True)
    account_type = models.CharField(max_length=200, null=True)

    def __str__(self): 
        return str(self.account_name)

# Create your models here.
class Customer(models.Model): 
    """this model handles the store users"""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    activate = models.BooleanField(default=False)
    address_info_complete = models.BooleanField(default=False) 
    banking_info_complete = models.BooleanField(default=False)
    profile_pic = models.ImageField(default='default.jpeg', null=True, blank=True, upload_to='images/profile_pics')
    date_created =  models.DateTimeField(auto_now_add=True, null=True)
    sponsor = models.CharField(max_length=200, null=True, blank=True)
    bank = models.OneToOneField(Banking, null=True, blank=True, on_delete=models.CASCADE)
    #address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.CASCADE)
    proof_of_activation_fee = models.ImageField(null=True, blank=True, upload_to='images/proof_of_payment')


    def __str__(self): 
        return str(self.username)

    @property
    def activation_proofURL(self):
        """this function solves the error associated with empty image fields"""
        try:
            url = self.proof_of_activation_fee.url
        except:
            url = ''
        return url
    
    
    @property
    def check_ref_bonus(self):
        reffs = Customer.objects.filter(sponsor=self.username)
        latest_max_setting = ReferralBonus.objects.all().order_by('-date').first()

        total_ref_spending = []
        for reff in reffs:
            total_ref_spending.append(float(reff.total_user_investments) * 0.03)
        sum_of_refs = sum(total_ref_spending)
        
        if int(sum_of_refs) > int(latest_max_setting.amount):
            return latest_max_setting.amount
        else:
            return sum_of_refs

    @property
    def total_user_investments(self):
        investments = []
        total_investments = HelpTable.objects.filter(approval_status='Approved')  

        for total_investment in total_investments:
            if total_investment.provider == self.username:
                investments.append(int(total_investment.amount)) 
        return sum(investments)
            

    @property
    def total_user_withdrawals(self):
        investments = []
        total_investments = HelpTable.objects.filter(approval_status='Approved') 
        
        for total_investment in total_investments:
            if total_investment.receiver == self.username:
                investments.append(int(total_investment.amount)) 
        return sum(investments)
        
    @property
    def total_downlines(self):
        downlines = Customer.objects.filter(sponsor=self.username).count()
        return downlines

    @property
    def total_returns(self):
        latest_percentage_returns_setting = PercentageReturn.objects.all().order_by('-date').first()
        latest = float(latest_percentage_returns_setting.amount) * 0.01
        latest_setting = float(1) + float(latest)

        return self.total_user_investments * latest_setting


    @property
    def net_balance(self):
        amount = self.check_ref_bonus + self.total_returns
        return amount - self.total_user_withdrawals


    @property
    def check_user_eligibility(self):
        if self.net_balance < 0:
            return False
        else:
            return True
 

    @property
    def check_user_PH_balance(self):
        amount_list = []
        amount2_list = []

        investments = HelpTable.objects.filter(provider=self.username).order_by('merge_date')
        
        #loop through the amount2 column and add each amount to investment list
        for investment in investments:
            amount_list.append(investment.amount)
            amount2_list.append(investment.amount2)

        #pick the last on the list
        try:
            last_PH_merge = amount_list[-1]
            last_PH_request = amount2_list[-1]
        except:
            last_PH_merge = 0
            last_PH_request = 0
        #initialize last PH merge and requests to zero if value is none
        if last_PH_merge is None:
            last_PH_merge = 0

        if last_PH_request is None:
            last_PH_request = 0

        #compute the balance left after PH
        balance_after_PH = int(last_PH_request) - int(last_PH_merge)
        
        return balance_after_PH



class HelpTable(models.Model):

    APPROVAL = (
        ('Approved', 'Approved'),
        ('Not Approved', 'Not Approved'),
        ('Fake', 'Fake'),
    )

    receiver = models.CharField(max_length=400, null=True, blank=True)
    provider = models.CharField(max_length=400, null=True, blank=True)
    amount = models.CharField(max_length=400, null=True, blank=True)
    amount2 = models.CharField(max_length=400, null=True, blank=True)
    approval_status = models.CharField(max_length=200, null=True, blank=True, choices=APPROVAL, default='Not Approved')
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    merge_date = models.DateTimeField(auto_now_add=True, null=True)
    #down_payment_status = models.CharField(max_length=200, null=True, blank=True, choices=DOWNPAYMENT, default='Not Paid')
    user_proof = models.ImageField(null=True, blank=True, upload_to='images/proof_of_payment')
    #admin_proof = models.ImageField(null=True, blank=True, upload_to='images/proof_of_payment')

    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_help_amount(self):
        """This property calculates the 10% down payment for each help"""
        
        get_amount = self.amount
       
        return get_amount

    @property
    def get_provider_phone(self):
        data = self.provider
        provider_details = Customer.objects.get(username=data)
        number = provider_details.phone_number
        return number

    @property
    def user_proofURL(self):
        """this function solves the error associated with empty image fields"""
        try:
            url = self.user_proof.url
        except:
            url = ''
        return url


class ReceiverTable(models.Model):
    APPROVAL = (
        ('Approved', 'Approved'),
        ('Not Approved', 'Not Approved'),
    )
    receiver = models.CharField(max_length=400, null=True, blank=True)    
    amount = models.CharField(max_length=400, null=True, blank=True)    
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, blank=True, choices=APPROVAL, default='Approved')
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.receiver)

    


class Merge(models.Model):
    STATUS = (
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
       
    )

    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default='Manual')
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.status)


class MinimumPH(models.Model):
    amount = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.amount)


class MaxPH(models.Model):
    amount = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.amount)

class PercentageReturn(models.Model):
    amount = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.amount)

"""
class DownPaymentPercentage(models.Model):
    amount = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.amount)
"""


class DaystoGH(models.Model):
    amount = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.amount)


class ReferralBonus(models.Model):
    amount = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.amount) 


class AdminAccountSetting(models.Model):
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    account_name = models.CharField(max_length=200, null=True, blank=True)
    account_number = models.CharField(max_length=200, null=True, blank=True)
    account_type = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.account_name)


class ActivationFeeSetting(models.Model):
    STATUS = (
        ('Admin', 'Admin'),
        ('Referrer', 'Referrer'),
    )
    option = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default='Admin')
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.option)
