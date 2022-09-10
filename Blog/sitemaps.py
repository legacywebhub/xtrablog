from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Post

class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'Blog:contact', 
            'Blog:about',
            'Blog:login',
            'Blog:blog',
            'Blog:newsletter',
        ]

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()