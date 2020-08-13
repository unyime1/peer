from django.urls import path

from . import views


urlpatterns = [ 
    path('admin/customer_page/<str:user_id>/', views.customerDetailsPage, name='customer_page'),  
    path('admin/admin_panel/', views.adminDashboard, name='admin_panel'),
    path('admin/all_users/', views.userList, name='all_users'),
    path('admin/banned_users/', views.bannedUsers, name='banned_users'),
    path('admin/site_settings/', views.Settings, name='settings'),
    path('admin/complete_merge/', views.mergeList, name='complete_merge'),

    path('admin/site_settings/merge_settings/', views.mergeChoice, name='merge_settings'),
    path('admin/site_settings/min_help_settings/', views.minHelp, name='min_help_settings'),
    path('admin/site_settings/max_help_settings/', views.maxHelp, name='max_help_settings'),
    path('admin/site_settings/returns_settings/', views.returnsonInv, name='returns_settings'),
    #path('admin/site_settings/downpaymentsset/', views.downpaymentsset, name='downpaymentsset'),
    path('admin/site_settings/daystogethelp/', views.daystogethelp, name='daystogethelp'),
    path('admin/site_settings/referralbonus/', views.referralbonus, name='referralbonus'),
    path('admin/site_settings/account_details/', views.accountDetailsSettings, name='account_details'),
    path('admin/site_settings/activation_fee_setting/', views.activationFeeSetting, name='activation_fee_setting'),
    path('admin/activation_fee_receipts/', views.activation_fee_receipts, name='activation_fee_receipts'),
    

    path('admin/get_help_requests/', views.getHelpRequests, name='get_help_requests'),
    path('admin/provide_help_requests/', views.provideHelpRequests, name='provide_help_requests'),
    path('admin/approved_help_history/', views.approvedHelpHistory, name='approved_help_history'),
    path('admin/support_requests/', views.supportRequests, name='support_requests'),
    path('admin/merge_customers/', views.mergeCustomers, name='merge_customers'),
    path('admin/block/<str:user_id>/', views.blockUser, name='block_user'),
    path('admin/delete/<str:user_id>/', views.deleteUser, name='delete_user'),
    path('admin/unblock/<str:user_id>/', views.unblockUser, name='unblock_user'),
    #path('admin/approve_down_payment/<str:help_id>/', views.approveDownPayment, name='approve_down_payment'),
    path('admin/approve_help/<str:help_id>/', views.approveHelp, name='approve_help'),
    path('admin/approve_withdrawal/<str:help_id>/', views.approveWithdrawal, name='approve_withdrawal'),
    path('admin/fake_help_reports/', views.fakeHelpReports, name='fake_help_reports'),
    path('admin/approve_activation/<str:user_id>/', views.aproveActivation, name='approve_activation'),

]