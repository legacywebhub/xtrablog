from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class XtraBlog(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email1 = models.EmailField(max_length=50, blank=False, null=False)
    email2 = models.EmailField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    whatsapp  = models.CharField(max_length=25, blank=True, null=True, help_text='whatsapp number')
    whatsapp_link  = models.CharField(max_length=200, blank=True, null=True)
    facebook_link  = models.CharField(max_length=200, blank=True, null=True)
    instagram_link  = models.CharField(max_length=200, blank=True, null=True)
    twitter_link  = models.CharField(max_length=200, blank=True, null=True)
    linked_in = models.CharField(max_length=200, blank=True, null=True)
    youtube_link = models.CharField(max_length=200, blank=True, null=True)
    newsletter_password = models.CharField(max_length=200, blank=True, null=True)
    google_analytics = models.TextField(max_length=2000, blank=True, null=True)
    retangular_ad = models.TextField(max_length=2000, blank=True, null=True)
    square_ad = models.TextField(max_length=2000, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id and XtraBlog.objects.exists():
            raise ValueError('This model cannot have more than one row or objects')
        else:
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images/users',blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=750, blank=True, null=True)

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
    ('online business', 'Online Business'),
    ('lifestyle', 'Lifestyle'),
    ('sports', 'Sports'),
    ('politics', 'Politics'),
    ('health', 'Health'),
    ('science', 'Science'),
    ('art', 'Art'),
    ('news', 'News'),
    ('commercial', 'Commercial'),
    ('entertainment', 'Entertainment'),
    ('programming', 'Programming'),
    ('how tos', 'How tos'),
    ('educational', 'Educational'),
    ('others', 'Others')
    )
    category_name =models.CharField(max_length=50,  choices=CATEGORY, primary_key=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, db_constraint=False, blank=False, null=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    image1 = models.ImageField(upload_to='images/blog', blank=True, null=True)
    image1_url = models.URLField(max_length=3000, blank=True, null=True)
    image2 = models.ImageField(upload_to='images/blog', blank=True, null=True)
    image2_url = models.URLField(max_length=3000, blank=True, null=True)
    image3 = models.ImageField(upload_to='images/blog', blank=True, null=True)
    image3_url = models.URLField(max_length=3000, blank=True, null=True)
    video = models.FileField(upload_to='videos', blank=True, null=True)
    video_url = models.URLField(max_length=3000, blank=True, null=True)
    youtube = models.TextField(max_length=3000, blank=True, null=True, help_text='Youtube video embedded code')
    document = models.FileField(upload_to='documents', blank=True, null=True)
    content = RichTextField(max_length=25000, blank=False, null=False)
    meta_keywords = models.CharField(max_length=150, blank=False, null=True)
    meta_description = models.CharField(max_length=250, blank=False, null=True)

    @property
    def new(self):
        status = False
        if self.id == Post.objects.last().id:
            status = True
        return status
    

    @property
    def total_comments(self):
        comments = self.comment_set.all()
        total = sum([item.number for item in comments])
        return total

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/article/{self.id}/'
        
    
class Comment(models.Model):
    number = models.PositiveIntegerField(default=1, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(max_length=3000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            name = self.user.username
        elif self.name:
            name = self.name
        else:
            name = '-'
        return name

    @property
    def total_replies(self):
        replies = self.reply_set.all()
        total = sum([item.number for item in replies])
        return total

    
class Reply(models.Model):
    number = models.PositiveIntegerField(default=1, editable=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    reply = models.TextField(max_length=3000, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def reply_user(self):
        if self.user:
            return self.user.username
        else:
            return self.name

    def __str__(self):
        return f'{self.date} {self.reply_user}'


class Subscriber(models.Model):
    email = models.EmailField(max_length=100)
    date_subscibed = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date)