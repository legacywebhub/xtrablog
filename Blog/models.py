from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class PostCategory(models.Model):
    CATEGORY = (
    ('business', 'Business'),
    ('web', 'Web Development'),
    ('graphics', 'Graphic design'),
    ('technology', 'Technology'),
    ('internet', 'Internet'),
    ('tutorials', 'Tutorials'),
    ('finance', 'Finance'),
    ('monetary', 'Monetary'),
    ('online-business', 'Online Business'),
    ('lifestyle', 'Lifestyle'),
    ('python', 'Python'),
    ('javascript', 'Javascript'),
    ('sports', 'Sports'),
    ('politics', 'Politics'),
    ('health', 'Health'),
    ('science', 'Science'),
    ('entertainment', 'Entertainment'),
    ('life-hacks', 'Life hacks'),
    )
    category_name =models.CharField(max_length=50,  choices=CATEGORY, primary_key=True)

    def __str__(self):
        return self.category_name


class Post(models.Model): 
    new = models.BooleanField(default=True) 
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, db_constraint=False, blank=False, null=True)
    slug = models.CharField(max_length=200, blank=False, null=False)
    date = models.DateTimeField(default=datetime.now)
    image1 = models.ImageField(upload_to='Images/blog', blank=True, null=True)
    image1_url = models.CharField(max_length=3000, blank=True, null=True)
    image2 = models.ImageField(upload_to='Images/blog', blank=True, null=True)
    image2_url = models.CharField(max_length=3000, blank=True, null=True)
    image3 = models.ImageField(upload_to='Images/blog', blank=True, null=True)
    image3_url = models.CharField(max_length=3000, blank=True, null=True)
    video = models.FileField(upload_to='Videos', blank=True, null=True)
    video_url = models.CharField(max_length=3000, blank=True, null=True)
    youtube = models.CharField(max_length=3000, blank=True, null=True)
    document = models.FileField(upload_to='Documents', blank=True, null=True)
    paragraph1 = models.TextField(max_length=10000, blank=False, null=False)
    paragraph2 = models.TextField(max_length=10000, blank=True, null=True)
    paragraph3 = models.TextField(max_length=10000, blank=True, null=True)
    paragraph4 = models.TextField(max_length=10000, blank=True, null=True)
    paragraph5 = models.TextField(max_length=10000, blank=True, null=True)
    link = models.CharField(max_length=3000, blank=True, null=True)
    link_description = models.CharField(max_length=250, blank=True, null=True)
    meta_keywords = models.CharField(max_length=150, blank=False, null=True)
    meta_description = models.CharField(max_length=160, blank=False, null=True)
    
    def __str__(self):
        return self.slug

    @property
    def total_comments(self):
        comments = self.comment_set.all()
        total = sum([item.number for item in comments])
        return total
        
    
class Comment(models.Model):
    number = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.user.username
    
    