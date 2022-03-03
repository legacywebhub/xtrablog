from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(XtraBlog)
admin.site.register(Message)
admin.site.register(Subscriber)
admin.site.register(MailMessage)
