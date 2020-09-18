"""this module holds the mains app views"""

from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages

# Create your views here.

def home(request):
    """this function handles the home page"""

    if request.method == 'POST':
        #get both the username and password
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
        )
        contact.save()
        
        messages.info(request, 'Hello ' + name.title() + ' Your message has been sent')
        return redirect('home')

    context = {}
    return render(request, 'mains/index.html', context)