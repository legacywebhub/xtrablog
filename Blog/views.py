from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.http import JsonResponse, HttpResponse
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
#pip install django-pandas
from django_pandas.io import read_frame

# Create your views here.
def login(request):
    contact = XtraBlog.objects.first()
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


def posts(request):
    p = Paginator(Post.objects.all(), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    contact = XtraBlog.objects.first()
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
    context = {'posts': posts, 'contact':contact, 'categories':categories}
    return render(request, 'index.html', context)


def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    related_posts = Post.objects.filter(category=post.category).order_by('?')[:3]
    comments = Comment.objects.filter(post=post)
    contact = XtraBlog.objects.first()
    categories = PostCategory.objects.all()
    user = request.user

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
        elif 'comment-submit' in request.POST:
            comment = request.POST['comment']
            if user.is_authenticated:
                comment = Comment(user=user, post=post, comment=comment)
                comment.save()
            else:
                name = request.POST['name']
                email = request.POST['email']
                try:
                    email.index('@') and email.index('.')
                except ValueError:
                    messages.error(request, 'Email is invalid!')
                else:
                    try:
                        len(name) > 50 and len(comment) > 3000
                    except True:
                        messages.error(request, 'Name or comment length exceeded maximum limit')
                    else:
                        comment = Comment(name=name, email=email,  post=post, comment=comment)
                        comment.save()
                        messages.info(request, 'Comment posted successfully')
        elif 'reply-submit' in request.POST:
            reply = request.POST['reply']
            if user.is_authenticated:
                reply = Reply(user=user, comment=comment, reply=reply)
                reply.save()
            else:
                name = request.POST['name']
                email = request.POST['email']
                comment_id = request.POST['comment']
                comment = Comment.objects.get(id=comment_id)
                try:
                    email.index('@') and email.index('.')
                except ValueError:
                    messages.error(request, 'Email is invalid!')
                else:
                    try:
                        len(name) > 25 and len(reply) > 3000
                    except True:
                        messages.error(request, 'Name or comment length exceeded maximum limit of 25 and 3000 respectively')
                    else:
                        reply = Reply(name=name, email=email,  comment=comment, reply=reply)
                        reply.save()
                        messages.info(request, 'Reply posted successfully')
    context = {
        'post' : post, 'comments':comments, 'contact':contact,
        'related_posts':related_posts, 'categories':categories
    }
    return render(request, 'post.html', context)



def result(request, search):
    results = Post.objects.filter(slug__contains=search) or Post.objects.filter(category=search)
    p = Paginator(results, 8)
    page = request.GET.get('page')
    posts = p.get_page(page)
    contact = XtraBlog.objects.first()
    categories = PostCategory.objects.all()

    if request.method == "POST":
        if 'search-submit' in request.POST:
            search = request.POST['search']
            messages.info(request, 'Search results for '+"'"+search+"'")
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
    context = {'posts':posts,'contact':contact, 
    'categories':categories, 'search':search}
    return render(request, 'results.html', context)


def newsletter(request):
    contact = XtraBlog.objects.first()
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

def contact(request):
    contact = XtraBlog.objects.first()
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
                send_mail(f'{subject} from {name}',message,email,['paulsonbosah@gmail.com', contact.email1, contact.email2])
                message = Message.objects.create(name=name, email=email, subject=subject, message=message)
                message.save()
                messages.info(request, f'Thanks {name}, we recieved your message and will respond shortly...')
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


def error_404(request, exception):
    contact = XtraBlog.objects.first()
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
    contact = XtraBlog.objects.first()
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