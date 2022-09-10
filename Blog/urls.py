from django.urls import path
from . import views as blogViews
from .sitemaps import StaticViewSitemap, PostSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
    'post': PostSitemap
}

app_name='Blog'
urlpatterns = [
    path('', blogViews.posts, name='blog'),
    path('result/<str:search>', blogViews.result, name='result'),
    path('article/<str:id>', blogViews.post, name='post'),
    path('contact/', blogViews.contact, name='contact'),
    path('about/', blogViews.about, name='about'),
    path('login/', blogViews.login, name='login'),
    path('logout/', blogViews.logout, name='logout'),
    path('newsletter/', blogViews.newsletter, name='newsletter'),
    path('sitemap.xml/', sitemap, {'sitemaps':sitemaps}),
]