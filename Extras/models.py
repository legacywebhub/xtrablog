from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=25, blank=False)
    whatsapp  = models.IntegerField(blank=True, null=True)
    whatsapp_link  = models.CharField(max_length=200, blank=True)
    facebook_link  = models.CharField(max_length=200, blank=True)
    instagram_link  = models.CharField(max_length=200, blank=True)
    twitter_link  = models.CharField(max_length=200, blank=True)
    linked_in = models.CharField(max_length=200, blank=True)
    youtube_link = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Subscriber(models.Model):
    email = models.EmailField(max_length=100)
    date_subscibed = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

class MailMessage(models.Model):
    title = models.CharField(max_length=1000, blank=False, null=False)
    message = models.TextField(max_length=3000, blank=False, null=False)

    def __str__(self):
        return self.title

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date)