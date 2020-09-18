"""this module holds the mains app models"""

from django.db import models

# Create your models here.

class Contact(models.Model):
    """this class handles the contact form table"""
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    message = models.CharField(max_length=20000, null=True)
    date_created =  models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
