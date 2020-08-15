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
        customer_username =  instance.username 

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
        customer_username = instance.username
        

        message_html = render_to_string('users/telegram_message_on_activation.html', {

            'customer_username':customer_username,

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        #photo =  instance.activation_proofURL

        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
        #bot.sendPhoto(chat_id="@%s" % telegram_settings['channel_name'], photo=photo)
post_save.connect(send_message_on_activation, sender=Customer) 


def send_message_on_PH(sender, instance, created, **kwargs):
    """send welcome message to new members"""   

    if created:
        provider = instance.provider
        amount = instance.amount

        message_html = render_to_string('users/telegram_message_on_ph.html', {
            'provider':provider,
            'amount':amount,

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_PH, sender=HelpTable) 


def send_message_on_PH_Merge(sender, instance, **kwargs):
    """send welcome message to new members"""
    
    if instance.receiver and instance.approval_status == "Not Approved" and not instance.user_proof:
        provider = instance.provider
        receiver = instance.receiver
        amount = instance.amount

        message_html = render_to_string('users/telegram_message_on_ph_merge.html', {
            'provider':provider,
            'receiver':receiver,
            'amount':amount

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_PH_Merge, sender=HelpTable) 


def send_message_on_PH_proof_submit(sender, instance, **kwargs):
    """send welcome message to new members"""
        
    if instance.approval_status == "Not Approved" and instance.user_proof:
        provider = instance.provider
        receiver = instance.receiver
        amount = instance.amount
       

        message_html = render_to_string('users/send_message_on_PH_proof_submit.html', {
            'provider':provider,
            'receiver':receiver,
            'amount':amount,
            
        })
        #photo =  instance.user_proofURL
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
        text=message_html, parse_mode=telegram.ParseMode.HTML)
        #bot.sendPhoto(chat_id="@%s" % telegram_settings['channel_name'], photo=photo)
post_save.connect(send_message_on_PH_proof_submit, sender=HelpTable)



def send_message_on_confirmed_PH(sender, instance, **kwargs):
    """send welcome message to new members"""
        
    if instance.approval_status == "Approved":
        provider = instance.provider
        receiver = instance.receiver

        amount = instance.amount

        message_html = render_to_string('users/telegram_message_on_confirmed_PH.html', {
            'provider':provider,
            'receiver':receiver,
            'amount':amount,

        })
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=message_html, parse_mode=telegram.ParseMode.HTML)
post_save.connect(send_message_on_confirmed_PH, sender=HelpTable) 
