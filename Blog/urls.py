from django.urls import path
from . import views as blogViews
from Extras import views as extraViews
from User import views as userViews


app_name='Blog'
urlpatterns = [
    path('', blogViews.posts, name='blog'),
    path('result/<str:search>', blogViews.result, name='result'),
    path('article/<str:post_id>', blogViews.post, name='post'),
    path('update/', blogViews.updatePostStatus, name='update'),
    path('contact/', extraViews.contact, name='contact'),
    path('about/', extraViews.about, name='about'),
    path('error/', extraViews.error_404, name='404'),
    path('login/', userViews.login, name='login'),
    path('logout/', userViews.logout, name='logout'),
    path('newsletter/', extraViews.newsletter, name='newsletter')
]