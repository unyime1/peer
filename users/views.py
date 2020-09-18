"""this module handles the users app views""" 

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import uuid
from datetime import datetime, timedelta, timezone, date
from django.views.decorators.csrf import ensure_csrf_cookie
import random

from .forms import *
from .email import *
from mains.decorators import *
# Create your views here.

 
@unauthenticated_users
def userRegistration(request):
    """this function handles the register view"""
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        #checks if form submission is valid
        if form.is_valid():
            form.save()

            #activate send mail function
            #send_activation_mail(request, user=user, form=form)

            #query username for flash message
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            messages.success(request, 'Hello ' + first_name + ' ' + last_name + ', your account has been created. Please go ahead and login.')
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form':form,}
    return render(request, 'users/register.html', context)



def activateAccount(request, uidb64, token):
    """this function activates the user account"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.info(request, 'Congrats, your email has been verified. Add your contact address. Please note that you cannot change this information later.')
        return redirect('address')
    else:
        return HttpResponse('Activation link is invalid!')



@login_required(login_url='login')
def addAddress(request):
    """this function handles the address view"""
    customer = request.user.customer
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            #address = form.cleaned_data['address']
            #city = form.cleaned_data['city']
            #state = form.cleaned_data['state']
            phone_number = form.cleaned_data['phone_number']
            sponsor = form.cleaned_data['sponsor']
            
            #Address.objects.create(
            #    customer=customer,
            #    address=address,
            #    city=city,
            #    state=state
            #)

            customer_update = Customer.objects.get(username=customer.username)
            customer_update.phone_number = phone_number
            customer_update.sponsor = sponsor
            customer_update.address_info_complete = True
            customer_update.save()

            messages.success(request, 'Please submit your banking information.')
            return redirect('bank')
    else:
        form = AddressForm()

    context = {'form':form,}
    return render(request, 'users/address_form.html', context)



@login_required(login_url='login')
def addBank(request):
    """this function handles the bank view"""
    form = BankingForm()
    if request.method == "POST":
        form = BankingForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.customer = request.user.customer
            bank.save()

            customer = request.user.customer
            customer.banking_info_complete = True
            customer.save()
            messages.success(request, 'Hello ' + customer.first_name.title() + ', your banking information has been saved. Thank you for joining us! ')
            
            return redirect('profile')
    else:
        form = BankingForm()

    context = {'form':form,}
    return render(request, 'users/bank_form.html', context)



@ensure_csrf_cookie
@unauthenticated_users
def userLogin(request):
    """this function handles the login view"""
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            #authenticate the user
            user = authenticate(request, username=username, password=password)

            #login user
            if user is not None:
                login(request, user)

                if user.customer.address_info_complete == False:
                    messages.error(request, 'Hello ' +  username + ', let us know more about you.')
                    return redirect('address')

                if user.customer.banking_info_complete == False:
                    messages.error(request, 'Hello ' +  username + ', please save your banking data!')
                    return redirect('bank')
                
                if user.customer.address_info_complete and user.customer.banking_info_complete:
                    messages.success(request, 'Hello ' +  username + ', you are now logged in.')
                    return redirect('profile')
                
            else:
                messages.error(request, 'Your username or password is incorrect!')
                return redirect('login')
                
    else:
        form = LoginForm()

    context = {'form':form,}
    return render(request, 'users/login.html', context)



@login_required(login_url='login')
def userLogout(request):
    """this function handles the logout functionality"""

    logout(request)
    return redirect('home')


@activation_fee
@login_required(login_url='login')
def proofOfPayment(request):
    """this view handles the submission of payment proofs."""
    customer = request.user.customer
    payments = HelpTable.objects.filter(provider=customer.username, approval_status="Not Approved")

    form = ProofOfPaymentForm()
    if request.method == "POST":
        form = ProofOfPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            transaction_id = form.cleaned_data['transaction_id']
            image = form.cleaned_data['image']

            help_data = HelpTable.objects.get(transaction_id=transaction_id)
            if help_data.receiver:
                help_data.user_proof = image
                help_data.save()
                messages.success(request, 'Your proof of payment has been submitted for approval.')
                return redirect('profile')
            else:
                messages.error(request, 'You have not been merged yet. Please wait a few more hours')
                return redirect('profile')
    else:
        form = ProofOfPaymentForm()

    context = {'customer':customer, 'form':form, 'payments':payments}
    return render(request, 'users/upload_proof.html', context)

"""
@login_required(login_url='login')
def adminProofOfPayment(request):
  
    customer = request.user.customer
    payments = HelpTable.objects.filter(provider=customer.username, down_payment_status="Not Paid")
    latest_account_details_setting = AdminAccountSetting.objects.all().order_by('-date').first()

    form = ProofOfPaymentForm()
    if request.method == "POST":
        form = ProofOfPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            transaction_id = form.cleaned_data['transaction_id']
            image = form.cleaned_data['image']

            help_data = HelpTable.objects.get(transaction_id=transaction_id)
            help_data.admin_proof = image
            help_data.save()
 
            messages.success(request, 'Your proof of payment has been submitted for approval. You will be merged shortly')
            return redirect('profile')
    else:
        form = ProofOfPaymentForm() 

    context = {'customer':customer, 'form':form, 'payments':payments,
        'latest_account_details_setting':latest_account_details_setting
    }
    return render(request, 'users/admin_proof.html', context)
"""

@login_required(login_url='login')
def updateBank(request):
    """this view handles the address update view"""

    customer = request.user.customer
    bank = Banking.objects.get(customer=customer)
    form = BankingForm(instance=bank)
    if request.method == "POST":
        form = BankingForm(request.POST, instance=bank)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.customer = customer
            bank.save()

            messages.success(request, 'Hi ' + customer.first_name.title() + ', your banking information has been updated')
            return redirect('profile')
    else:
        form = BankingForm(instance=bank)

    context = {'customer':customer, 'form':form, }
    return render(request, 'users/bank_form.html', context)



@login_required(login_url='login')
def customerSupport(request):
    """this function handles the customer support view"""
    customer = request.user.customer
    form = SupportForm()
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.name = customer.username
            complaint.email = customer.email
            complaint.phone = customer.phone_number
            complaint.save()

            messages.success(request, 'Hi ' + customer.first_name.title() + ', your message has been forwarded to us. We will get back to you shortly.')
            return redirect('profile')
    else:
        form = SupportForm()

    context = {'form':form, 'customer':customer, }
    return render(request, 'users/support.html', context)


@activation_fee
@login_required(login_url='login')
def userReferrals(request):
    """this view handles user referrals"""
    customer = request.user.customer
    #pull all the downlines for this user from the database
    downlines = Customer.objects.filter(sponsor=customer.username)
    total_count_of_downlines = downlines.count()

    context = {'customer':customer, 'downlines':downlines, 'total_count_of_downlines':total_count_of_downlines,}
    return render(request, 'users/referrals.html', context)


@activation_fee
@login_required(login_url='login')
def userWithdrawalHistory(request):
    """this view handles withdrawal History"""
    customer = request.user.customer
    #pull receiver data from database database
    withdrawals = HelpTable.objects.filter(receiver=customer).order_by('-merge_date')
    total_withdrawals_count = withdrawals.count()


    context = {'customer':customer, 'withdrawals':withdrawals, 'total_withdrawals_count':total_withdrawals_count,}
    return render(request, 'users/withdrawal_history.html', context)


@activation_fee
@login_required(login_url='login')
def userApproveHelp(request, withdrawal_id):
    """this function handles help approval"""
    helps = HelpTable.objects.get(id=withdrawal_id)

    #check if help has a proof of payment
    if not helps.user_proof:
        messages.error(request, 'Helper must upload proof of payment before help can be approved.')
        return redirect('profile')
    else:
        helps.approval_status = "Approved"
        helps.save()
        messages.success(request, 'Your approval is successfull')
    return redirect('admin_panel') 



@activation_fee
@login_required(login_url='login')
def userReportHelp(request, withdrawal_id):
    """this function handles the report of help"""
    helps = HelpTable.objects.get(id=withdrawal_id)
    helps.approval_status = "Fake"
    helps.save()

    #search for and activate the customer that provided help
    help_provider = helps.provider
    customer = Customer.objects.get(username=help_provider)
    customer.activate = True
    customer.save()

    messages.success(request, 'Your report is successfull')
    return redirect('profile')
    

@activation_fee
@login_required(login_url='login')
def userWithdrawalPage(request):
    """this view handles the Investment withdrawal Page"""
    customer = request.user.customer
    latest_days_setting = DaystoGH.objects.all().order_by('-date').first()

    form = GetHelpForm()
    #initialize a list
    investment_list = []
    investment_dates = []
    #pull all user's investments
    investments = HelpTable.objects.filter(provider=customer).order_by('merge_date')
    #loop through the investments and add each amount to investment list
    for investment in investments:
        investment_list.append(int(float(investment.amount)))
        investment_dates.append(investment.merge_date)
    #identify the largest value
    try:
        largest_investment = max(investment_list) #get largest
        total_investment = sum(investment_list) #set sum
        last_investment = investment_list[-1] #get last
        last_investment_date = investment_dates[-1] #get last investment date
        time_betw = datetime.now(timezone.utc) - last_investment_date #get the difference between now and the date of last investment 
             
    except:
        largest_investment = 1
        total_investment = 1
        last_investment = 1
        last_investment_date = datetime.now()
        time_betw = last_investment_date - datetime.now()
        pass

    if request.method == "POST":
        form = GetHelpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            #if the number of days elapsed is less than the minimum set in site settings
            if int(time_betw.days) < int(latest_days_setting.amount):
                messages.warning(request, 'Hello ' + customer.first_name.title() + ', your last investment has not matured yet. Wait a few more hours before trying again. ')
                return redirect('withdrawal_page')
            if int(amount) > int(largest_investment):
                messages.warning(request, 'Hello ' + customer.first_name.title() + ', the highest amount you have invested is ₦' + str(largest_investment) + '. At the moment, you cannot withdraw above that.')
                return redirect('withdrawal_page')
            if int(amount) > int(total_investment):
                messages.warning(request, 'Hello ' + customer.first_name.title() + ', your total investment on our platform is ' + str(total_investment) + '. You cannot make a single withdrawal above that amount.')
                return redirect('withdrawal_page')
            if customer.check_user_eligibility == False:
                messages.warning(request, 'Hello ' + customer.first_name.title() + ', you can no longer get help on our platform. Please provide help first! ')
                return redirect('withdrawal_page')
            
            else:
                ReceiverTable.objects.create(
                    receiver=customer.username,
                    amount=amount,
                )
            messages.success(request, 'Hello ' + customer.first_name.title() + ', thanks for believing in us. You will be paired with another user shortly.')
            return redirect('profile')
    else:
        form = GetHelpForm()

    context = {
        'form':form, 'customer':customer,
    }
    return render(request, 'users/withdrawal_page.html', context)


@activation_fee
@login_required(login_url='login')
def investmentHistory(request):
    """this view handles the Investment History Page"""
    customer = request.user.customer

    #pull receiver data from database database
    investments = HelpTable.objects.filter(provider=customer).order_by('-merge_date')
    total_investments_count = investments.count()

    context = {
        'customer':customer, 'investments':investments, 'total_investments_count':total_investments_count, 
    }
    return render(request, 'users/investment_history.html', context)


@activation_fee
@login_required(login_url='login')
def investmentPage(request):
    """this view handles the Investment Page"""
    customer = request.user.customer
    form = ProvideHelpForm()
    my_id = uuid.uuid4()
    transaction_id = my_id.node
    
    #initialize a list
    investment_list = []
    #pull all user's investments
    investments = HelpTable.objects.filter(provider=customer.username)
    #loop through the investments and add each amount to investment list
    for investment in investments:
        investment_list.append(investment.amount)
    #identify the largest value
    try:
        largest_investment = max(investment_list)
    except ValueError:
        largest_investment = 1

    if request.method == "POST":
        form = ProvideHelpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            

            if int(amount) < int(float(largest_investment)):
                messages.warning(request, 'Hello ' + customer.first_name.title() + ', the highest amount you have invested is ₦' + str(largest_investment) + '. You cannot invest an amount below this. Please input a higher amount.')
                return redirect('investment_page')
            if int(amount) < 5000:
                messages.warning(request, 'Hello ' + customer.first_name.title() + ', you cannot invest an amount below ₦5000 on our platform. Please input a higher amount.')
                return redirect('investment_page')
            if int(amount) > 100000:
                messages.warning(request, 'Hello ' + customer.first_name.title() + ', you cannot invest an amount above ₦100000 on our platform. Please input a lower amount.')
                return redirect('investment_page')
            else:

                HelpTable.objects.create(
                    provider=customer.username,
                    amount=amount,
                    amount2=amount,
                    transaction_id=transaction_id,
                    )

                #automatic merging logic
                #username of provider
                helps = HelpTable.objects.get(transaction_id=transaction_id)
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
                            help_table = HelpTable.objects.filter(approval_status="Not Approved", amount=receive_amount).first()
                            #if such exists,merge the two users.
                            help_table.receiver = receive.receiver
                            receive.complete = True
                            receive.save()
                            help_table.save()
                        except:
                           
                            #initialize and array of eligible provide help requests
                            user_array = []
                            #save the receiver to help table if receiver wants amount greater than help. Keep help amount the same
                            if int(receive_amount) > int(helps.amount):
                                helps.receiver = receive.receiver
                                helps.save()

                                #take the remaining
                                remaining = int(receive_amount) - int(helps.amount)
                                
                                try:

                                    #query help table again
                                    help_table = HelpTable.objects.filter(approval_status="Not Approved")
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
                                user_array2 = []
                                #split receive amount into 2
                                user_amount = int(receive_amount) / 2
                                
                                
                                #sort through the table and add provider usernames to list
                                help_table = HelpTable.objects.filter(approval_status="Not Approved")
                                for helps in help_table:
                                    user_array2.append(helps)
                                #pick 2 random objects from the array.
                                
                                #get 2 random objects from array
                                try:
                                    random_sample = random.sample(user_array2, 2)
                                    for randoms in random_sample:
                                        randoms.receiver = receive.receiver
                                        randoms.amount = user_amount
                                        randoms.save()
                                        receive.complete = True
                                        receive.save()
                                #if not upto 2, get the only one
                                except:
                                    random_sample = random.choice(user_array2)
                                    randoms.receiver = receive.receiver
                                    randoms.amount = user_amount
                                    random.save()
                                    receive.complete = True
                                    receive.save()
                            
                messages.success(request, 'Hello ' + customer.first_name.title() + ', thanks for investing with us. You will be merged soon.')
                return redirect('profile')

    else:
        form = ProvideHelpForm()
     
    context = {
        'largest_investment':largest_investment, 'customer':customer, 'form':form
    }
    return render(request, 'users/investment_page.html', context)



@login_required(login_url='login')
def mergeDetailsPage(request):
    """this function handles the view that shows merge details"""
    #get customer
    customer = request.user.customer
    #check the help table and get row which has this customer as provider
    details = HelpTable.objects.filter(provider=customer.username, approval_status="Not Approved").order_by('-merge_date').first()
    #from the row, pull receiver. Receiver is stored with username
    receiver = details.receiver
    
    #search for customers with that username
    receiving_customer = Customer.objects.get(username=receiver)

    context = {
        'customer':customer, 'receiving_customer':receiving_customer, 'details':details,
    }
    return render(request, 'users/merge_details_page.html', context)



@login_required(login_url='login')
def withdrawalDetailsPage(request):
    """this function handles the receiver details"""
    #get customer
    customer = request.user.customer
    #check the help table and get row which has this customer as provider
    details = HelpTable.objects.filter(receiver=customer.username, approval_status="Not Approved").order_by('-merge_date').first()
    #from the row, pull receiver. Receiver is stored with username
    provider = details.provider
    
    #search for customers with that username
    providing_customer = Customer.objects.get(username=provider)

    context = {
        'customer':customer, 'providing_customer':providing_customer, 'details':details,
    }
    return render(request, 'users/receive_details_page.html', context)



@login_required(login_url='login')
def userDashboard(request):
    """this function handles the user dashboard""" 

    customer = request.user.customer
    #account details stuff
    latest_act_fee_setting = ActivationFeeSetting.objects.all().order_by('-date').first()
    if latest_act_fee_setting == "Admin":    
        latest_account_details_setting = AdminAccountSetting.objects.all().order_by('-date').first()
    else:
        try:
            sponsor = customer.sponsor
            
            sponsor_profile = Customer.objects.get(username=sponsor)

            latest_account_details_setting = sponsor_profile.bank
        except:
            latest_account_details_setting = AdminAccountSetting.objects.all().order_by('-date').first()
    
        downlines = Customer.objects.filter(sponsor=customer.username, activate=False)


    help_data = HelpTable.objects.filter(provider=customer.username, approval_status="Not Approved").order_by('-merge_date').first()
    receive_data = HelpTable.objects.filter(receiver=customer.username, approval_status="Not Approved").order_by('-merge_date').first()
    
    context = {'customer':customer, 'help_data':help_data, 'latest_account_details_setting':latest_account_details_setting,
        'receive_data':receive_data, 'downlines':downlines,
        }
    return render(request, 'users/dashboard.html', context)



@login_required(login_url='login')
def proofOfActivationPay(request):
    """this function handles proof of activation fee submission"""
    customer = request.user.customer
    form = ActivationProofForm()
    if request.method == "POST":
        form = ActivationProofForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            user = Customer.objects.get(username=customer.username)
            user.proof_of_activation_fee = image
            user.save()

            messages.success(request, 'Hi ' + customer.first_name.title() + ', your proof of activation has been submitted. We will review and activate your account shortly.')
            return redirect('profile')
    else:
        form = ActivationProofForm()

    context = {'customer':customer, 'form':form, }
    return render(request, 'users/proof_of_act_form.html', context)



def activation_fee_receipts_user(request):
    """this page handles the activation fee receipts page"""
    customer = request.user.customer
    inactive_customers = Customer.objects.filter(activate=False, sponsor=customer.username)
    
    context = {'inactive_customers':inactive_customers,}
    return render(request, 'users/activation_fee_receipts.html', context)


