from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(Subscriber)
admin.site.register(MailMessage)