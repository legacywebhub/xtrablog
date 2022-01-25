from django.shortcuts import render, redirect
from Blog.models import *
from Extras.models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def login(request):
    contact = Contact.objects.first()
    categories = PostCategory.objects.all()

    if request.method == "POST":
        if 'search-submit' in request.POST:
            search = request.POST['search']
            messages.info(request, 'Search results for '+'"'+search+'"')
            return redirect('/result/'+search)
        elif 'subscribe-submit' in request.POST:   
            subscribe = request.POST['subscribe']
            subscribed = Subscriber.objects.filter(email=subscribe).exists()
            if subscribed == True:   
                messages.info(request, 'Email has already been subscribed!')
            else:
                subscribe = Subscriber(email=subscribe)
                subscribe.save()
                messages.info(request, 'Thanks for subscribing!')
        elif 'register-submit' in request.POST:
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username taken')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    messages.info(request, 'Your account was successfully created... you can sign in now')
            else:
                messages.error(request, 'Passwords do not match')
        elif 'login-submit' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            print(username)
            print(password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Welcome'+ user.username)
                return redirect('/')
            else:
                messages.error(request, 'Invalid credentials')
    context = {'contact':contact, 'categories':categories,}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    messages.info(request, 'Thanks... we wish to see you soon again')
    return redirect('/')