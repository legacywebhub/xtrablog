from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
import json
from django.contrib import messages
from django.core.paginator import Paginator
from Extras.models import *

# Create your views here.
def posts(request):
    p = Paginator(Post.objects.filter(new=False), 4)
    page = request.GET.get('page')
    posts = p.get_page(page)
    latest_posts = Post.objects.filter(new=True).order_by('?')[:4]
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
    context = {'posts': posts, 'contact':contact,
    'latest_posts':latest_posts, 'categories':categories}
    return render(request, 'index.html', context)

def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    related_posts = Post.objects.filter(category=post.category).order_by('?')[:3]
    comments = post.comment_set.all()
    contact = Contact.objects.first()
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
                        messages.info(request, 'Comment posted successfully')
    context = {
        'post' : post, 'comments':comments, 'contact':contact,
        'related_posts':related_posts, 'categories':categories
    }
    return render(request, 'post.html', context)


def updatePostStatus(request):
    posts = Post.objects.filter(new=True)
    response = json.dumps({'posts':posts})

    if request.method == "POST":
        data = json.loads(request.body)
        action = data['update']

        if update == 'true':
            for post in posts:
                post.new = False
                return JsonResponse('post status updated', safe=False)
        else:
            pass


def result(request, search):
    results = Post.objects.filter(slug__contains=search) or Post.objects.filter(category=search)
    p = Paginator(results, 8)
    page = request.GET.get('page')
    posts = p.get_page(page)
    contact = Contact.objects.first()
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