from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random

from .forms import *
from .models import *
from users.models import *
from mains.models import *
from mains.decorators import *


# Create your views here.

@admin_only
@login_required(login_url='login') 
def adminDashboard(request):
    """this function handles the admin dashboard view"""
    users_count = User.objects.all().count()
    
    help_amounts = HelpTable.objects.filter(approval_status='Approved')
    total_help_given_list = []
    total_help_received_list = []
    for helps in help_amounts: 
        total_help_given_list.append(int(helps.amount))
        total_help_received_list.append(int(helps.amount))   
    total_help_given = sum(total_help_given_list)
    total_help_received = sum(total_help_received_list)

    context = {
        'users_count':users_count, 'total_help_given':total_help_given, 'total_help_received':total_help_received
    }
    return render(request, 'admins/dashboard.html', context)



@admin_only
@login_required(login_url='login')
def userList(request):
    """this function handles the user list view"""
    users = User.objects.filter(is_active=True)
    inactive_customers = Customer.objects.filter(activate=False)
    inactive_members_count = inactive_customers.count()

    user_count = users.count()

    context = {'users':users, 'user_count':user_count, "inactive_customers":inactive_customers,
    'inactive_members_count':inactive_members_count

    }
    return render(request, 'admins/all_users.html', context)


@admin_only
@login_required(login_url='login')
def aproveActivation(request, user_id):
    user = Customer.objects.get(id=user_id)
    user.activate = True
    user.save()
    messages.success(request, 'Your approval was successfull')
    return redirect('admin_panel')



@admin_only
@login_required(login_url='login')
def bannedUsers(request):
    """this function handles the banned users view"""
    users = User.objects.filter(is_active=False)
    users_count = users.count()

    context = {'users':users, 'users_count':users_count}
    return render(request, 'admins/banned_users.html', context)



@admin_only
@login_required(login_url='login')
def blockUser(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, 'Your block was successfull')
    return redirect('admin_panel')



@admin_only
@login_required(login_url='login')
def unblockUser(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, 'Your unblock was successfull')
    return redirect('admin_panel')



@admin_only
@login_required(login_url='login')
def deleteUser(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, 'Your delete was successfull')
    return redirect('admin_panel')



@admin_only
@login_required(login_url='login')
def Settings(request):

    latest_merge_setting = Merge.objects.all().order_by('-date').first()
    latest_min_ph_setting = MinimumPH.objects.all().order_by('-date').first()
    latest_max_ph_setting = MaxPH.objects.all().order_by('-date').first()
    latest_percentage_returns_setting = PercentageReturn.objects.all().order_by('-date').first()
    #latest_downpayments_setting = DownPaymentPercentage.objects.all().order_by('-date').first()
    latest_days_setting = DaystoGH.objects.all().order_by('-date').first()
    latest_bonus = ReferralBonus.objects.all().order_by('-date').first()
    latest_account_details_setting = AdminAccountSetting.objects.all().order_by('-date').first()
    activation_fee_setting = ActivationFeeSetting.objects.all().order_by('-date').first()

    context = { #'latest_downpayments_setting':latest_downpayments_setting,
        'latest_merge_setting':latest_merge_setting, 'latest_min_ph_setting':latest_min_ph_setting,
        'latest_max_ph_setting':latest_max_ph_setting, 'latest_percentage_returns_setting':latest_percentage_returns_setting,
         'latest_days_setting':latest_days_setting, 
        'latest_bonus':latest_bonus, 'latest_account_details_setting':latest_account_details_setting,
        'activation_fee_setting':activation_fee_setting

    }
    return render(request, 'admins/settings.html', context) 


@admin_only
@login_required(login_url='login')
def mergeChoice(request):

    latest_merge_setting = Merge.objects.all().order_by('-date').first()

    form = MergeForm()
    if request.method == 'POST':
        form = MergeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = MergeForm()

    context = {'form':form, 'latest_merge_setting':latest_merge_setting}
    return render(request, 'admins/merge_choice.html', context) 
    

@admin_only
@login_required(login_url='login')
def minHelp(request):
    latest_min_ph_setting = MinimumPH.objects.all().order_by('-date').first()
    
    form = MinimumPHForm()
    if request.method == 'POST':
        form = MinimumPHForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = MinimumPHForm()

    context = {'form':form, 'latest_min_ph_setting':latest_min_ph_setting}
    return render(request, 'admins/min_help.html', context) 



@admin_only
@login_required(login_url='login')
def maxHelp(request):
    latest_max_ph_setting = MaxPH.objects.all().order_by('-date').first()
    
    form = MaxPHForm()
    if request.method == 'POST':
        form = MaxPHForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = MaxPHForm()

    context = {'form':form, 'latest_max_ph_setting':latest_max_ph_setting,}
    return render(request, 'admins/max_help.html', context) 


@admin_only
@login_required(login_url='login')
def returnsonInv(request):
    latest_percentage_returns_setting = PercentageReturn.objects.all().order_by('-date').first()
    
    form = PercentageReturnForm()
    if request.method == 'POST':
        form = PercentageReturnForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = PercentageReturnForm()

    context = {'form':form, 'latest_percentage_returns_setting':latest_percentage_returns_setting,}
    return render(request, 'admins/return_on_inv.html', context) 

"""
#removed per client request
@admin_only
@login_required(login_url='login')
def downpaymentsset(request):
    latest_downpayments_setting = DownPaymentPercentage.objects.all().order_by('-date').first()
    
    form = DownPaymentForm()
    if request.method == 'POST':
        form = DownPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = DownPaymentForm()

    context = {'form':form, 'latest_downpayments_setting':latest_downpayments_setting,}
    return render(request, 'admins/downpayment.html', context) 
"""

@admin_only
@login_required(login_url='login')
def daystogethelp(request):
    latest_days_setting = DaystoGH.objects.all().order_by('-date').first()
    
    form = DaysToGHForm()
    if request.method == 'POST':
        form = DaysToGHForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = DaysToGHForm()

    context = {'form':form, 'latest_days_setting':latest_days_setting ,}
    return render(request, 'admins/days2gh.html', context) 


@admin_only
@login_required(login_url='login')
def accountDetailsSettings(request):
    latest_account_details_setting = AdminAccountSetting.objects.all().order_by('-date').first()
    
    form = AdminAccountSettingForm()
    if request.method == 'POST':
        form = AdminAccountSettingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = AdminAccountSettingForm()

    context = {'form':form, 'latest_account_details_setting':latest_account_details_setting,}
    return render(request, 'admins/account_details_setting.html', context) 



@admin_only
@login_required(login_url='login')
def referralbonus(request):
    latest_bonus = ReferralBonus.objects.all().order_by('-date').first()
    
    form = ReferralBonusForm()
    if request.method == 'POST':
        form = ReferralBonusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = ReferralBonusForm()

    context = {'form':form, 'latest_bonus':latest_bonus,}
    return render(request, 'admins/referralbonusset.html', context) 


@admin_only
@login_required(login_url='login')
def getHelpRequests(request):
    """this function handles the get help request view"""

    helps = ReceiverTable.objects.all().order_by('-date')

    context = {'helps':helps,}
    return render(request, 'admins/get_help_requests.html', context)



@admin_only
@login_required(login_url='login')
def provideHelpRequests(request):
    """this function handles the provide help request view"""
    helps = HelpTable.objects.all().order_by('-merge_date')

    context = {'helps':helps,}
    return render(request, 'admins/provide_help_requests.html', context)


@admin_only
@login_required(login_url='login')
def fakeHelpReports(request):
    """this function handles the provide help request view"""
    helps = HelpTable.objects.filter(approval_status='Fake').order_by('-merge_date')

    context = {'helps':helps,}
    return render(request, 'admins/fake_help_reports.html', context)


"""
@admin_only
@login_required(login_url='login')
def approveDownPayment(request, help_id):
    helps = HelpTable.objects.get(id=help_id)
    helps.down_payment_status = "Paid"
    
    
    #automatic merging logic
    #username of provider
    help_provider = helps.provider
    
    #get latest merge setting
    latest_merge_setting = Merge.objects.all().order_by('-date').first()
    
    #get the oldest user on receive table
    receive = ReceiverTable.objects.filter(status="Approved").order_by('date').first()
    
    if latest_merge_setting.status == "Automatic":

        #check if there is an approved help request.
        if receive:
            #init random
            global random
            
            #get receive amount
            receive_amount = receive.amount
            #query help table for receive amount, paid down payment, and unapproved approval status
            try:
                help_table = HelpTable.objects.get(down_payment_status="Paid", approval_status="Not Approved", amount=receive_amount)
                #if such exists,merge the two users.
                help_table.receiver = receive.receiver
                receive.complete = True
                receive.save()
                help_table.save()
            except:
                pass
            
            #initialize and array of eligible provide help requests
            user_array = []
            #save the reciver to help table if receiver wants amount greater than help. Keep help amount the same
            if int(receive_amount) > int(helps.amount):
                helps.receiver = receive.receiver
                helps.save()

                #take the remaining
                remaining = int(receive_amount) - int(helps.amount)
                
                try:

                    #query help table again
                    help_table = HelpTable.objects.filter(down_payment_status="Paid", approval_status="Not Approved")
                    for helps in help_table:
                        user_array.append(helps)

                    try:
                        #choose any provider from the provider table to provide the remaining balance
                        user = random.choice(user_array)
                        user.receiver = receive.receiver
                        user.amount = remaining
                        user.save()
                        receive.complete = True
                        receive.save()
                    except:
                        pass
                except:
                    pass
                
            if int(receive_amount) < int(helps.amount):
                helps.receiver = receive.receiver
                helps.amount = receive_amount
                helps.save()
                receive.complete = True
                receive.save()
                
            #in every other situations not handlesd above
            else:
                #split receive amount into 2
                user_amount = int(receive_amount) / 2
                
                
                #sort through the table and add provider usernames to list
                help_table = HelpTable.objects.filter(down_payment_status="Paid", approval_status="Not Approved")
                for helps in help_table:
                    user_array.append(helps)
                #pick 2 random objects from the array.
                
                #get 2 random objects from array
                try:
                    random_sample = random.sample(user_array, 2)
                    for randoms in random_sample:
                        randoms.receiver = receive.receiver
                        randoms.amount = user_amount
                        randoms.save()
                        receive.complete = True
                        receive.save()
                #if not upto 2, get the only one
                except:
                    random_sample = random.choice(user_array)
                    randoms.receiver = receive.receiver
                    randoms.amount = user_amount
                    random.save()
                    receive.complete = True
                    receive.save()
    

    messages.success(request, 'Your approval is successful')
    return redirect('admin_panel')
"""


@admin_only
@login_required(login_url='login')
def approveHelp(request, help_id):
    helps = HelpTable.objects.get(id=help_id) 

    #check that proof of payment and receiveris available before help is approved
    if not helps.user_proof:
        messages.error(request, 'Helper must upload proof of payment before help can be approved.')
        return redirect('admin_panel')
    if helps.receiver is None:
        messages.error(request, 'There must be a receiver for help to be approved')
        return redirect('admin_panel')
    else:
        helps.approval_status = "Approved"
        helps.save()
        messages.success(request, 'Your approval is successfull')
    return redirect('admin_panel') 




@admin_only
@login_required(login_url='login')
def approveWithdrawal(request, help_id):
    helps = ReceiverTable.objects.get(id=help_id)

    helps.status = 'Approved'
    helps.save()
    messages.success(request, 'Your approval is successfull')
    return redirect('admin_panel')



@admin_only
@login_required(login_url='login')
def approvedHelpHistory(request):
    """this function handles the approved help history view"""

    helps = HelpTable.objects.filter(approval_status='Approved')
    total_approved = helps.count()

    context = {'helps':helps, 'total_approved':total_approved}
    return render(request, 'admins/approved_help_history.html', context)



@admin_only
@login_required(login_url='login')
def supportRequests(request):
    """this function handles the approved help history view"""
    supports = Contact.objects.all().order_by('-date_created')

    context = {'supports':supports, }
    return render(request, 'admins/support_requests.html', context)



@admin_only
@login_required(login_url='login')
def customerDetailsPage(request, user_id):
    """this function handles the approved help history view"""
    user = User.objects.get(id=user_id)

    context = {'user':user}
    return render(request, 'admins/customer_details_page.html', context)


@admin_only
@login_required(login_url='login')
def mergeCustomers(request):
    """this function handles the approved help history view"""
    form = MergeCustomersForm()

    if request.method == "POST":
        form = MergeCustomersForm(request.POST)

        if form.is_valid():
            provider = form.cleaned_data['provider']
            receiver = form.cleaned_data['receiver']
            amount = form.cleaned_data['amount']
            transaction_id = form.cleaned_data['transaction_id'] 

            merge_help = HelpTable.objects.get(transaction_id=transaction_id)
            merge_help.provider = provider
            merge_help.receiver = receiver
            merge_help.amount = amount
            merge_help.transaction_id = transaction_id

            merge_help.save()

            messages.success(request, 'The merge is saved. The users involved have been notified.')
            return redirect('admin_panel')
    else:
        form = MergeCustomersForm()

    context = {'form':form,}
    return render(request, 'admins/merge_customers.html', context)



@admin_only
@login_required(login_url='login')
def mergeList(request):
    """this function handles the approved help history view"""
    helps = HelpTable.objects.all().order_by('-merge_date')

    context = {'helps':helps,}
    return render(request, 'admins/merge_list.html', context)


@login_required(login_url='login')
def activationFeeSetting(request):
    activation_fee_setting = ActivationFeeSetting.objects.all().order_by('-date').first()
    
    form = ActivationFeeSettingForm()
    if request.method == 'POST':
        form = ActivationFeeSettingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings has been saved')
            return redirect('admin_panel')
            
    else:
        form = ActivationFeeSettingForm()

    context = {'form':form, 'activation_fee_setting':activation_fee_setting,}
    return render(request, 'admins/activation_fee_setting.html', context) 


@login_required(login_url='login')
def activation_fee_receipts(request):
    """this page handles the activation fee receipts page"""

    inactive_customers = Customer.objects.filter(activate=False)
    
    

    context = {'inactive_customers':inactive_customers}
    return render(request, 'admins/activation_fee_receipts.html', context)