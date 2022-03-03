from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Images/users', default='Images/users/default.jpg', blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    whatsapp  = models.IntegerField(blank=True, null=True)
    whatsapp_link  = models.URLField(max_length=200, blank=True, null=True)
    facebook_link  = models.URLField(max_length=200, blank=True, null=True)
    instagram_link  = models.URLField(max_length=200, blank=True, null=True)
    twitter_link  = models.URLField(max_length=200, blank=True, null=True)
    linked_in = models.URLField(max_length=200, blank=True, null=True)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    rectangular_ad1 = models.TextField(max_length=2000, blank=True, null=True)
    rectangular_ad2 = models.TextField(max_length=2000, blank=True, null=True)
    square_ad = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.user.username
class PostCategory(models.Model):
    CATEGORY = (
    ('business', 'Business'),
    ('technology', 'Technology'),
    ('internet', 'Internet'),
    ('tutorials', 'Tutorials'),
    ('finance', 'Finance'),
    ('monetary', 'Monetary'),
    ('online-business', 'Online Business'),
    ('lifestyle', 'Lifestyle'),
    ('sports', 'Sports'),
    ('politics', 'Politics'),
    ('health', 'Health'),
    ('science', 'Science'),
    ('entertainment', 'Entertainment'),
    ('programming', 'Programming'),
    ('how-to', 'How-to'),
    ('educational', 'Educational')
    )
    category_name =models.CharField(max_length=50,  choices=CATEGORY, primary_key=True)

    def __str__(self):
        return self.category_name


class Post(models.Model): 
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, db_constraint=False, blank=False, null=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    image1 = models.ImageField(upload_to='Images/blog', blank=True, null=True)
    image1_url = models.URLField(max_length=3000, blank=True, null=True)
    image2 = models.ImageField(upload_to='Images/blog', blank=True, null=True)
    image2_url = models.URLField(max_length=3000, blank=True, null=True)
    image3 = models.ImageField(upload_to='Images/blog', blank=True, null=True)
    image3_url = models.URLField(max_length=3000, blank=True, null=True)
    video = models.FileField(upload_to='Videos', blank=True, null=True)
    video_url = models.URLField(max_length=3000, blank=True, null=True)
    youtube = models.URLField(max_length=3000, blank=True, null=True)
    document = models.FileField(upload_to='Documents', blank=True, null=True)
    content = RichTextField(max_length=25000, blank=False, null=False)
    link = models.CharField(max_length=3000, blank=True, null=True)
    link_description = models.CharField(max_length=250, blank=True, null=True)
    meta_keywords = models.CharField(max_length=150, blank=False, null=True)
    meta_description = models.CharField(max_length=160, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return f'/article/{self.id}'

    @property
    def total_comments(self):
        comments = self.comment_set.all()
        total = sum([item.number for item in comments])
        return total
        
    
class Comment(models.Model):
    number = models.PositiveIntegerField(default=1, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

    @property
    def total_replies(self):
        replies = self.reply_set.all()
        total = sum([item.number for item in replies])
        return total
    
class Reply(models.Model):
    number = models.PositiveIntegerField(default=1, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField(max_length=3000, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def reply_user(self):
        if user:
            return user.username
        else:
            return name

    def __str__(self):
        return f'{date} {reply_user}'

class XtraBlog(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email1 = models.EmailField(max_length=50, blank=False, null=False)
    email2 = models.EmailField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=25, blank=True)
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

class SubscribersMail(models.Model):
    title = models.CharField(max_length=1000, blank=False, null=False)
    image = models.FileField(upload_to="Images/subscribers", blank=True, null=True)
    message = models.TextField(max_length=3000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

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