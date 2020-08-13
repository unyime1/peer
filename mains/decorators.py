"""This module handles user permissions"""
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

 
def unauthenticated_users(view_func):
    """this decorator is used to give access to unauthenticated users only"""
    def  wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def activation_fee(view_func):
    """this decorator is used to give access to unauthenticated users only"""
    def  wrapper_func(request, *args, **kwargs):
        customer = request.user.customer
        if customer.activate:
            return view_func(request, *args, **kwargs)
            
        else:
            messages.error(request, 'Please activate your account first.')
            return redirect('profile')
    return wrapper_func


def allowed_users(allowed_roles=[]):
    """this function handles user permissions"""
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs): 
            group = None #usergroup initialized to none
            if request.user.groups.exists():   #check to see if the user is included in any group
                group = request.user.groups.all()[0].name # if he is, pick the first one and store in the group variable
            if group in allowed_roles: #if his group is among the allowed roles
                return view_func(request, *args, **kwargs) #return the required view
            else:
                return HttpResponse('You are not authorized to view this page!!!') #if not, prevent access
        return wrapper_func #return the view
    return decorator


def admin_only(view_func):
    """this decorator ensures that a particular page is viewed by the admin only"""
    def wrapper_func(request, *args, **kwargs): 
        group = None #usergroup initialized to none
        if request.user.groups.exists():   #check to see if the user is included in any group
            group = request.user.groups.all()[0].name # if he is, pick the first one and store in the group variable

        if group == 'admin':
            return view_func(request, *args, **kwargs) #return requested view if user is admin

        else:
            return redirect('profile') #else, redirect to userpage

    return wrapper_func 