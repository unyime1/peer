from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
#admin.site.register(Address)
admin.site.register(Banking)
admin.site.register(HelpTable)
admin.site.register(Merge)
admin.site.register(ReceiverTable)
admin.site.register(MinimumPH)
admin.site.register(MaxPH)
admin.site.register(PercentageReturn)

