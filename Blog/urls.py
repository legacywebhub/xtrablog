from django.urls import path
from . import views as blogViews


app_name='Blog'
urlpatterns = [
    path('', blogViews.posts, name='blog'),
    path('result/<str:search>', blogViews.result, name='result'),
    path('article/<str:post_id>', blogViews.post, name='post'),
    path('contact/', blogViews.contact, name='contact'),
    path('about/', blogViews.about, name='about'),
    path('error/', blogViews.error_404, name='404'),
    path('login/', blogViews.login, name='login'),
    path('logout/', blogViews.logout, name='logout'),
    path('newsletter/', blogViews.newsletter, name='newsletter')
]