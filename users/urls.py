"""this module handles the users app urls""" 

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    path('profile/', views.userDashboard, name='profile'),
    path('register/', views.userRegistration, name='register'),
    path('address/', views.addAddress, name='address'),
    path('bank/', views.addBank, name='bank'),
    path('login/', views.userLogin, name='login'),
    path('activate/<uidb64>/<token>/', views.activateAccount, name='activate'),
    path('logout/', views.userLogout, name='logout'),
    path('proof/', views.proofOfPayment, name='proof'),
    #path('admin_proof/', views.adminProofOfPayment, name='admin_proof'),
    path('activate_proof/', views.proofOfActivationPay, name='activate_proof'),
    path('update_bank/', views.updateBank, name='update_bank'),
    path('support/', views.customerSupport, name='support'),
    path('referrals/', views.userReferrals, name='referrals'),
    path('withdrawal_history/', views.userWithdrawalHistory, name='withdrawal_history'),
    path('withdrawal_page/', views.userWithdrawalPage, name='withdrawal_page'),
    path('investment_history/', views.investmentHistory, name='investment_history'),
    path('investment_page/', views.investmentPage, name='investment_page'),
    path('user/merge_details/', views.mergeDetailsPage, name='merge_details'),
    path('user/receive_details_page/', views.withdrawalDetailsPage, name='receive_details_page'),
    path('user/user_approve_help/<str:withdrawal_id>/', views.userApproveHelp, name='user_approve_help'),
    path('user/user_report_help/<str:withdrawal_id>/', views.userReportHelp, name='user_report_help'),
    path('act_fee_user/', views.activation_fee_receipts_user, name='act_fee_user'),



    #password reset views
      path('password_reset/', auth_views.PasswordResetView.as_view(
          template_name="users/password_reset.html"
        ),
        name='password_reset'), #
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_sent.html"
        ),
        name='password_reset_done'), #
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_form.html"
        ),
        name='password_reset_confirm'), #
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_done.html"
        ),
        name='password_reset_complete'),    #

    #send email view
]