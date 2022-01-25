from django.shortcuts import render, redirect
from django.core.mail import send_mail
#pip install django-pandas
from django_pandas.io import read_frame
from Extras.models import *
from .models import *

# Create your views here.
def contact(request):
    contact = Contact.objects.first()
    if request.method == "POST":
        if 'message-submit' in request.POST:
            name = request.POST["name"]
            email = request.POST["email"]
            subject = request.POST["subject"]
            message = request.POST["message"]
            try:
                email.index('@') and email.index('.')
            except ValueError:
                messages.info(request, 'Your email is not valid')
            else:
                message = Message.objects.create(name=name, email=email, subject=subject, message=message)
                message.save()
                messages.info(request, f'Thanks {name}, we recieved your message and will respond shortly...')
                #send_mail(subject,message,email,['paulsonbosah@gmail.com'])
                return redirect('/contact/')
        elif 'subscribe-submit' in request.POST:
            subscribe = request.POST["subscribe"]
            subscribed = Subscriber.objects.filter(email=subscribe).exists()
            if subscribed == True:
                messages.info(request, 'This email has already been subscribed!')
            else:
                subscribe = Subscriber(email=subscribe)
                subscribe.save()
                messages.info(request, 'Thanks for subscribing!')
    return render(request, 'contact.html', {'contact':contact})


def newsletter(request):
    contact = Contact.objects.first()
    emails = Subscriber.objects.all()
    #the following line of codes converts the query to a list object
    #using the read_mail function from django-pandas external module
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    print(mail_list)

    if request.method=="POST":
        if 'newsletter-submit' in request.POST:
            # form = MailMessageForm(request.POST or None)
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, 'Message succesfully sent to mail list')
            #     title = form.cleaned_data.get('title')
            #     message = form.cleaned_data.get('message')
                send_mail(
                title, message, 'legacywebtech@gmail.com', mail_list, fail_silently=False
                )
                return redirect('/admin/')
        elif 'subscribe-submit' in request.POST:
            subscribe = request.POST['subscribe']
            subscribed = Subscriber.objects.filter(email=subscribe).exists()
            if subscribed == True:
                messages.info(request, 'This email has already been subscribed!')
            else:
                subscribe = Subscriber(email=subscribe)
                subscribe.save()
                messages.info(request, 'Thanks for subscribing!')
    # else:
    #     form = MailMessageForm()
    return render(request, 'newsletter.html', {'contact':contact})


def error_404(request, exception):
    contact = Contact.objects.first()
    if request.method=='POST':
        subscribe = request.POST['subscribe']
        subscribed = Subscriber.objects.filter(email=subscribe).exists()
        if subscribed == True:
            messages.info(request, 'This email has already been subscribed!')
        else:
            subscribe = Subscriber(email=subscribe)
            subscribe.save()
            messages.info(request, 'Thanks for subscribing!')
    return render(request, '404.html', {'contact':contact})


def about(request):
    contact = Contact.objects.first()
    if request.method=='POST':
        subscribe = request.POST['subscribe']
        subscribed = Subscriber.objects.filter(email=subscribe).exists()
        if subscribed == True:
            messages.info(request, 'This email has already been subscribed!')
        else:
            subscribe = Subscriber(email=subscribe)
            subscribe.save()
            messages.info(request, 'Thanks for subscribing!')
    return render(request, 'about.html', {'contact':contact,})