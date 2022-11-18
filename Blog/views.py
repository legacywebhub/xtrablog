from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.http import JsonResponse, HttpResponse
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage
#pip install django-pandas
from django_pandas.io import read_frame

# General variables
xtrablog = XtraBlog.objects.last()

# Create your views here.
def login(request):
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

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Signed in successfully... Welcome '+ user.username)
                return redirect('/')
            else:
                messages.error(request, 'Invalid credentials')
    context = {'xtrablog':xtrablog, 'categories':categories,}
    return render(request, 'login.html', context)



def logout(request):
    auth.logout(request)
    messages.info(request, 'Thanks... we wish to see you soon again')
    return redirect('/')



def posts(request):
    categories = PostCategory.objects.all()
    p = Paginator(Post.objects.all().order_by('-created_at'), 12)
    page = request.GET.get('page')
    posts = p.get_page(page)

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
    context = {'posts': posts, 'xtrablog':xtrablog, 'categories':categories}
    return render(request, 'index.html', context)



def post(request, id):
    post = get_object_or_404(Post, pk=id)
    related_posts = Post.objects.filter(category=post.category).order_by('?')[:3]
    comments = Comment.objects.filter(post=post)
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
        elif 'comment-submit' in request.POST:
            comment = request.POST['comment']
            if request.user.is_authenticated:
                comment = Comment(user=request.user, post=post, comment=comment)
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
                        messages.success(request, 'Comment posted successfully')
        elif 'reply-submit' in request.POST:
            comment_id = request.POST['comment']
            reply = request.POST['reply']
            comment = Comment.objects.get(id=comment_id)
            
            if request.user.is_authenticated:
                reply = Reply(user=request.user, comment=comment, reply=reply)
                reply.save()
            else:
                name = request.POST['name']
                email = request.POST['email']
                
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
                        messages.success(request, 'Reply posted successfully')
    context = {
        'post' : post, 'comments':comments, 'xtrablog':xtrablog,
        'related_posts':related_posts, 'categories':categories
    }
    return render(request, 'post.html', context)



def result(request, search):
    categories = PostCategory.objects.all()
    category_results = Post.objects.filter(category=search)
    title_results = Post.objects.filter(title__contains=search)
    results = []

    if category_results:
        for result in category_results:
            if result not in results:
                results.append(result)
    
    if title_results:
        for result in title_results:
            if result not in results:
                results.append(result)

    p = Paginator(results, 12)
    page = request.GET.get('page')
    posts = p.get_page(page)

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
    context = {'posts':posts,'xtrablog':xtrablog, 
    'categories':categories, 'search':search}
    return render(request, 'results.html', context)



def newsletter(request):
    categories = PostCategory.objects.all()
    # getting all subscribers
    emails = Subscriber.objects.all()
    # the following line of codes converts the query to a list object
    # using the read_mail function from django-pandas external module
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()

    if request.method=="POST":
        if 'newsletter-submit' in request.POST:
            password = request.POST['password']
            subject = request.POST['subject']
            message = request.POST['message']

            if password == xtrablog.newsletter_password:
                if file in request.POST:
                    file = request.POST['file']

                    try:
                        email = EmailMessage(subject, message, xtrablog.email1, mail_list)
                        email.content_subtype = 'html'
                        email.attach(file.name, file.read(), file.content_type)
                        email.send()
                        messages.success(request, 'Message and file succesfully sent to mail list')
                    except:
                        messages.error(request, 'Sorry... There was an error while forwarding newsletter and file')
                        
                else:
                    try:
                        send_mail(subject, message, xtrablog.email1, mail_list, fail_silently=False)
                        messages.success(request, 'Message succesfully sent to mail list')
                    except:
                        messages.error(request, 'Sorry... There was an error while forwarding newsletter')

            else:
                messages.error(request, 'Newsletter password is incorrect!')
        elif 'subscribe-submit' in request.POST:
            subscribe = request.POST['subscribe']
            subscribed = Subscriber.objects.filter(email=subscribe).exists()
            if subscribed == True:
                messages.info(request, 'This email has already been subscribed!')
            else:
                subscribe = Subscriber(email=subscribe)
                subscribe.save()
                messages.info(request, 'Thanks for subscribing!')
        elif 'search-submit' in request.POST:
            search = request.POST['search']
            messages.info(request, 'Search results for '+"'"+search+"'")
            return redirect('/result/'+search)
    return render(request, 'newsletter.html', {'xtrablog':xtrablog, 'categories':categories,})



def contact(request):
    categories = PostCategory.objects.all()
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
                send_mail(f'{subject} from {name}',message,email,[xtrablog.email1, xtrablog.email2])
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
        elif 'search-submit' in request.POST:
            search = request.POST['search']
            messages.info(request, 'Search results for '+"'"+search+"'")
            return redirect('/result/'+search)
    return render(request, 'contact.html', {'xtrablog':xtrablog,  'categories':categories,})



def error404(request, exception):
    categories = PostCategory.objects.all()
    if request.method=='POST':
        subscribe = request.POST['subscribe']
        subscribed = Subscriber.objects.filter(email=subscribe).exists()
        if subscribed == True:
            messages.info(request, 'This email has already been subscribed!')
        else:
            subscribe = Subscriber(email=subscribe)
            subscribe.save()
            messages.info(request, 'Thanks for subscribing!')
    return render(request, '404.html', {'xtrablog':xtrablog,  'categories':categories,})



def serverError(request):
    categories = PostCategory.objects.all()
    if request.method=='POST':
        subscribe = request.POST['subscribe']
        subscribed = Subscriber.objects.filter(email=subscribe).exists()
        if subscribed == True:
            messages.info(request, 'This email has already been subscribed!')
        else:
            subscribe = Subscriber(email=subscribe)
            subscribe.save()
            messages.info(request, 'Thanks for subscribing!')
    return render(request, '500.html', {'xtrablog':xtrablog, 'categories':categories,})



def about(request):
    categories = PostCategory.objects.all()
    if request.method=='POST':
        if 'subscribe-submit' in request.POST:
            subscribe = request.POST['subscribe']
            subscribed = Subscriber.objects.filter(email=subscribe).exists()
            if subscribed == True:
                messages.info(request, 'This email has already been subscribed!')
            else:
                subscribe = Subscriber(email=subscribe)
                subscribe.save()
                messages.info(request, 'Thanks for subscribing!')
        elif 'search-submit' in request.POST:
                search = request.POST['search']
                messages.info(request, 'Search results for '+"'"+search+"'")
                return redirect('/result/'+search)
    return render(request, 'about.html', {'xtrablog':xtrablog,  'categories':categories,})