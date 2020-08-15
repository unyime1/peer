from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
#telegram stuff
from django.template.loader import render_to_string
import telegram 
from django.conf import settings
from .models import *

 
def customer_profile(sender, instance, created, **kwargs):
    """this function handles the creation of users"""
    
    if created: #check if this is the first instance
        #add registered user to customer group
        group = Group.objects.get(name='customer') #query customer group in admin
        instance.groups.add(group)  #add instance of user to the queried group

        #to avoid errors when a registered user visits the user page, we have to add the user to the 'user' table of the Customer model
        Customer.objects.create(    #
            user=instance, 
            first_name = instance.first_name,
            last_name = instance.last_name,
            username = instance.username,
            email = instance.email,
        )

post_save.connect(customer_profile, sender=User) 


def send_message_on_registration(sender, instance, created, **kwargs):
    """send welcome message to new members"""

    if created:
        customer_first_name = instance.customer.first_name.capitalize()
        customer_last_name = instance.customer.last_name.capitalize()
        customer_username = instance.customer.username

        message_html = render_to_string('users/telegram_message_on_registration.html', {

            'customer_username':customer_username,

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_registration, sender=User) 


def send_message_on_activation(sender, instance, created, **kwargs):
    """send welcome message to new members"""
        
    if instance.activate:
        customer_first_name = instance.first_name.capitalize()
        customer_last_name = instance.last_name.capitalize()
        customer_username = instance.username

        message_html = render_to_string('users/telegram_message_on_activation.html', {

            'customer_username':customer_username,
            'customer_first_name':customer_first_name,
            'customer_last_name':customer_last_name


        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_activation, sender=Customer) 


def send_message_on_PH(sender, instance, created, **kwargs):
    """send welcome message to new members"""

    if created:
        provider = instance.provider
        amount = instance.amount
        profile = Customer.objects.get(username=provider)
        first_name = profile.first_name.capitalize()
        last_name = profile.last_name.capitalize()

        message_html = render_to_string('users/telegram_message_on_ph.html', {
            'first_name':first_name,
            'last_name':last_name,
            'amount':amount,

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_PH, sender=HelpTable) 


def send_message_on_PH_Merge(sender, instance, **kwargs):
    """send welcome message to new members"""
    
    if instance.receiver:
        provider = instance.provider
        receiver = instance.receiver

        amount = instance.amount
        profile = Customer.objects.get(username=provider)
        first_name = profile.first_name.capitalize()
        last_name = profile.last_name.capitalize()

        receiver_profile = Customer.objects.get(username=receiver)
        receiver_first_name = receiver_profile.first_name
        receiver_last_name = receiver_profile.last_name

        message_html = render_to_string('users/telegram_message_on_ph_merge.html', {
            'first_name':first_name,
            'last_name':last_name,
            'amount':amount,
            'receiver_first_name':receiver_first_name,
            'receiver_last_name':receiver_last_name

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_PH_Merge, sender=HelpTable) 



def send_message_on_confirmed_PH(sender, instance, **kwargs):
    """send welcome message to new members"""
        
    if instance.approval_status == "Approved":
        provider = instance.provider
        receiver = instance.receiver

        amount = instance.amount
        profile = Customer.objects.get(username=provider)
        first_name = profile.first_name.capitalize()
        last_name = profile.last_name.capitalize()

        receiver_profile = Customer.objects.get(username=receiver)
        receiver_first_name = receiver_profile.first_name
        receiver_last_name = receiver_profile.last_name

        message_html = render_to_string('users/telegram_message_on_confirmed_PH.html', {
            'first_name':first_name,
            'last_name':last_name,
            'amount':amount,
            'receiver_first_name':receiver_first_name,
            'receiver_last_name':receiver_last_name

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_confirmed_PH, sender=HelpTable) 


def send_message_on_PH_proof_submit(sender, instance, **kwargs):
    """send welcome message to new members"""
        
    if instance.approval_status == "Approved" and instance.user_proof:
        provider = instance.provider
        receiver = instance.receiver

        amount = instance.amount
        profile = Customer.objects.get(username=provider)
        first_name = profile.first_name.capitalize()
        last_name = profile.last_name.capitalize()

        receiver_profile = Customer.objects.get(username=receiver)
        receiver_first_name = receiver_profile.first_name
        receiver_last_name = receiver_profile.last_name

        message_html = render_to_string('users/send_message_on_PH_proof_submit.html', {
            'first_name':first_name,
            'last_name':last_name,
            'amount':amount,
            'receiver_first_name':receiver_first_name,
            'receiver_last_name':receiver_last_name

        })
        photo =  instance.user_proofURL
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
        text=message_html, parse_mode=telegram.ParseMode.HTML)
        bot.sendPhoto(chat_id="@%s" % telegram_settings['channel_name'], photo=photo)
post_save.connect(send_message_on_PH_proof_submit, sender=HelpTable)